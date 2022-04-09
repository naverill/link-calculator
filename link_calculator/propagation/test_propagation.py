from math import isclose, radians

import numpy as np

from link_calculator.constants import EARTH_RADIUS
from link_calculator.orbits.utils import angle_sat_to_gs_orbital_radius, slant_range
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
)
from link_calculator.propagation.utils import (
    free_space_loss_db,
    horizontal_reduction,
    power_density,
    rain_attenuation,
    rain_specific_attenuation,
    receive_power,
    slant_path,
    zeta,
)


def test_free_space_loss():
    orbital_radius = 42164
    frequency = 6  # GHz

    elevation_angles = [10, 90]
    path_loss = [200.17, 199.08]

    for angle, loss in zip(elevation_angles, path_loss):
        angle_sat_to_gs = angle_sat_to_gs_orbital_radius(
            orbital_radius, elevation=angle
        )

        srange = slant_range(orbital_radius, angle_sat_to_gs)
        loss_calc = abs(free_space_loss_db(srange, frequency))
        assert isclose(loss_calc, loss, rel_tol=0.05)


def test_rain_specific_attenuation_vertical():
    frequencies = [1, 2, 8, 15, 30]
    atts_k = [0.0000352, 0.000138, 0.00395, 0.0335, 0.167]
    atts_alpha = [0.880, 0.923, 1.310, 1.128, 1.000]

    for f, k, alpha in zip(frequencies, atts_k, atts_alpha):
        k_, alpha_, _ = rain_specific_attenuation(f, 0, polarization="vertical")

        assert isclose(k, k_, rel_tol=0.4)
        assert isclose(alpha, alpha_, rel_tol=0.4)


def test_rain_specific_attenuation_horizontal():
    frequencies = [1, 2, 8, 15, 30]
    atts_k = [0.0000387, 0.000154, 0.00454, 0.0367, 0.187]
    atts_alpha = [0.912, 0.963, 1.327, 1.154, 1.021]

    for f, k, alpha in zip(frequencies, atts_k, atts_alpha):
        k_, alpha_, _ = rain_specific_attenuation(f, 0, polarization="horizontal")

        assert isclose(k, k_, rel_tol=0.5)
        assert isclose(alpha, alpha_, rel_tol=0.5)


def test_rain_attenuation():
    freq = 4  # GHz
    rain_rate = 8  # mm / h
    gs_altitude = 0.5  # km
    gs_lat = 30
    elevation = 42  # deg
    rain_height = 2.45  # km

    polarizations = ["horizontal", "vertical", "circular"]
    rain_atts = [0.0229, 0.0193, 0.0211]
    spec_atts = [0.0067, 0.0055, 0.0061]
    horiz_reds = [1.4882, 1.4978, 1.4929]
    zetas = [31.1744, 31.1744, 31.1744]

    for i in range(len(polarizations)):
        _, _, att = rain_specific_attenuation(freq, rain_rate, polarizations[i])
        assert isclose(att, spec_atts[i], rel_tol=0.05)

        spath = slant_path(
            elevation,
            rain_height,
            gs_altitude,
        )
        assert isclose(spath, 2.9142, rel_tol=0.1)

        horiz_proj = spath * np.cos(radians(elevation))
        assert isclose(horiz_proj, 2.1657, rel_tol=0.01)
        horiz_red = horizontal_reduction(horiz_proj, att, freq)
        assert isclose(horiz_red, horiz_reds[i], rel_tol=0.01)

        zeta_ = zeta(rain_height, gs_altitude, horiz_proj, horiz_red)
        assert isclose(zeta_, zetas[i], rel_tol=0.01)

        rain_att = rain_attenuation(
            elevation,
            spath,
            freq,
            rain_height,
            gs_altitude,
            gs_lat,
            rain_rate,
            polarizations[i],
        )
        assert isclose(rain_att, rain_atts[i], rel_tol=0.1)


def test_rain_attenuation_2():
    freq = 12  # GHz
    rain_rate = 10  # mm / h
    gs_altitude = 0.6  # km
    gs_lat = 20
    elevation = 50  # deg
    rain_height = 3  # km

    k, alpha, att = rain_specific_attenuation(
        freq, rain_rate, polarization="horizontal"
    )

    assert isclose(k, 0.0188, rel_tol=0.05)
    assert isclose(alpha, 1.217, rel_tol=0.05)
    assert isclose(att, 0.3099, rel_tol=0.05)

    spath = slant_path(
        elevation,
        rain_height,
        gs_altitude,
    )
    assert isclose(spath, 3.1329, rel_tol=0.01)

    horiz_proj = spath * np.cos(radians(elevation))
    assert isclose(horiz_proj, 2.0138, rel_tol=0.01)
    horiz_red = horizontal_reduction(horiz_proj, att, freq)
    assert isclose(horiz_red, 1.2424, rel_tol=0.01)

    zeta_ = zeta(rain_height, gs_altitude, horiz_proj, horiz_red)
    assert isclose(zeta_, 43.8, rel_tol=0.01)

    rain_att = rain_attenuation(
        elevation,
        spath,
        freq,
        rain_height,
        gs_altitude,
        gs_lat,
        rain_rate,
        "horizontal",
    )
    assert isclose(rain_att, 1.241, rel_tol=0.1)


def test_received_power():
    sat_altitude = 40000 * 1000  # km
    transmit_gain = decibel_to_watt(17)  # dB
    transmit_power = 10  # W
    effective_app = 10  # m^2

    power_dens = power_density(transmit_power, transmit_gain, sat_altitude)
    assert isclose(power_dens, 2.49e-14, rel_tol=0.1)

    receive_power = power_dens * effective_app

    assert isclose(receive_power, 2.49e-13, rel_tol=0.1)


def test_received_power_2():
    sat_altitude = 40000 * 1000  # km
    transmit_gain = decibel_to_watt(17)  # dB
    transmit_power = 10  # W
    effective_app = 10  # m^2
    # frequency = 11  # GHz
    receive_gain = decibel_to_watt(52.3)  # dB

    wavelength = np.sqrt((4 * np.pi * effective_app) / receive_gain)
    assert isclose(wavelength, 2.727e-2, rel_tol=0.01)

    rec_power = receive_power(
        transmit_power,
        1,
        transmit_gain,
        sat_altitude,
        1,
        receive_gain,
        1,
        wavelength=wavelength,
    )
    assert isclose(watt_to_decibel(rec_power), -126.0, rel_tol=0.1)


def test_receive_power_3():
    transmit_power = 9  # W
    transmit_gain = decibel_to_watt(16)  # W
    transmit_loss = decibel_to_watt(-3)  # W
    distance = 24500 * 1000  # m

    receive_loss = decibel_to_watt(-2)  # W
    receive_gain = decibel_to_watt(57)  # W

    atmospheric_loss = decibel_to_watt(-9)  # W

    eff_aperture = None  # m^2
    wavelength = frequency_to_wavelength(11)  # m
    power = receive_power(
        transmit_power,
        transmit_loss,
        transmit_gain,
        distance,
        receive_loss,
        receive_gain,
        atmospheric_loss,
        wavelength,
        eff_aperture,
    )
    assert isclose(power, -133, rel_tol=0.01)


def test_receive_power_4():
    transmit_power = 6  # W
    transmit_gain = decibel_to_watt(18)  # W
    transmit_loss = 1  # W
    distance = 12000 * 1000  # m

    receive_loss = 1  # W
    receive_gain = 1  # W

    atmospheric_loss = 1  # W

    eff_aperture = 13  # m^2
    wavelength = None  # m

    power = receive_power(
        transmit_power,
        transmit_loss,
        transmit_gain,
        distance,
        receive_loss,
        receive_gain,
        atmospheric_loss,
        wavelength,
        eff_aperture,
    )
    assert isclose(power, -116, rel_tol=0.01)
