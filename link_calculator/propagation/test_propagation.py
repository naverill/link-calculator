from math import isclose, radians

import numpy as np

from link_calculator.components.antennas import Antenna
from link_calculator.constants import EARTH_RADIUS
from link_calculator.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
)
from link_calculator.orbits.utils import central_angle_orbital_radius, slant_range
from link_calculator.propagation.attenuation import (
    horizontal_reduction,
    rain_attenuation,
    rain_specific_attenuation,
    slant_path,
    zeta,
)


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
