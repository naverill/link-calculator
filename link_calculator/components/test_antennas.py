from math import degrees, isclose

import numpy as np

from link_calculator.components.antennas import (
    Amplifier,
    Antenna,
    ParabolicAntenna,
    SquareHornAntenna,
)
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
    wavelength_to_frequency,
)


def test_parabolic_antenna():
    efficiency_ = [1, 0.6]
    gain_ = [62.41, 60.19]

    for e, g in zip(efficiency_, gain_):
        ant = ParabolicAntenna(circular_diameter=9, efficiency=e, frequency=14)
        assert np.isclose(ant.wavelength, 0.02143, rtol=0.1)
        assert np.isclose(watt_to_decibel(ant.gain), g, rtol=0.1)


def test_parabolic_antenna_1():
    ant = ParabolicAntenna(circular_diameter=8, efficiency=0.5, frequency=7)
    assert np.isclose(watt_to_decibel(ant.gain), 52.4, rtol=0.1)


def test_square_horn_antenna():
    ant = SquareHornAntenna(cross_sect_diameter=0.07, efficiency=0.45, frequency=14)
    assert np.isclose(ant.wavelength, 0.02143, rtol=0.1)
    assert np.isclose(watt_to_decibel(ant.gain), 17.8, rtol=0.1)
    assert np.isclose(ant.half_beamwidth, 15.44, rtol=0.1)


def test_square_horn_antenna_1():
    ant = SquareHornAntenna(cross_sect_diameter=0.07, efficiency=0.45, frequency=12)
    assert np.isclose(watt_to_decibel(ant.gain), 16.47, rtol=0.1)
    assert np.isclose(ant.half_beamwidth, 18.0, rtol=0.1)


def test_pointing_loss():
    ant = Antenna(half_beamwidth=1)
    pointing_error = degrees(0.002)
    assert np.isclose(
        -watt_to_decibel(ant.pointing_loss(pointing_error)), 0.16, rtol=0.1
    )


def test_pointing_loss_1():
    ant = Antenna(half_beamwidth=2)
    pointing_error = degrees(0.005)
    assert np.isclose(
        -watt_to_decibel(ant.pointing_loss(pointing_error)), 0.246, rtol=0.1
    )


def test_received_power():
    sat_altitude = 40000  # km
    transmit_gain = decibel_to_watt(17)  # dB
    transmit_power = 10  # W
    effective_app = 10  # m^2

    amp = Amplifier(power=transmit_power)
    ant = Antenna(amplifier=amp, gain=transmit_gain)
    power_dens = ant.power_density_distance(sat_altitude)
    assert isclose(power_dens, 2.49e-14, rel_tol=0.1)

    receive_power = power_dens * effective_app

    assert isclose(receive_power, 2.49e-13, rel_tol=0.1)


def test_received_power_2():
    sat_altitude = 40000  # km

    receive_ant = Antenna(gain=decibel_to_watt(52.3), effective_aperture=10)
    wavelength = np.sqrt(
        (4 * np.pi * receive_ant.effective_aperture) / receive_ant.gain
    )
    amp = Amplifier(power=10)
    transmit_ant = Antenna(
        amplifier=amp, gain=decibel_to_watt(17), wavelength=wavelength
    )
    assert isclose(wavelength, 2.727e-2, rel_tol=0.01)
    rec_power = receive_ant.receive_power(
        transmit_ant,
        sat_altitude,
    )
    assert isclose(watt_to_decibel(rec_power), -126.0, rel_tol=0.1)


def test_receive_power_3():
    amp = Amplifier(power=9)
    transmit_ant = Antenna(
        amplifier=amp,
        gain=decibel_to_watt(16),
        loss=decibel_to_watt(-3),
    )
    distance = 24500  # km

    receive_ant = Antenna(
        gain=decibel_to_watt(57),
        loss=decibel_to_watt(-2),
        wavelength=frequency_to_wavelength(11),
    )
    atmospheric_loss = decibel_to_watt(-9)  # W

    power = receive_ant.receive_power(
        transmit_ant,
        distance,
        atmospheric_loss,
    )
    assert isclose(watt_to_decibel(power), -133, rel_tol=0.01)


def test_receive_power_4():
    amp = Amplifier(power=6)
    transmit_ant = Antenna(amplifier=amp, gain=decibel_to_watt(18), loss=1)
    distance = 12000  # km

    receive_ant = Antenna(gain=1, effective_aperture=13)

    power = receive_ant.receive_power(
        transmit_ant,
        distance,
    )
    assert isclose(watt_to_decibel(power), -116, rel_tol=0.01)
