from math import degrees

import numpy as np

from link_calculator.components.antennas import (
    Antenna,
    ParabolicAntenna,
    SquareHornAntenna,
)
from link_calculator.propagation.conversions import watt_to_decibel


def test_parabolic_antenna():
    efficiency_ = [1, 0.6]
    gain_ = [62.41, 60.19]

    for e, g in zip(efficiency_, gain_):
        ant = ParabolicAntenna(
            name="test", circular_diameter=9, efficiency=e, frequency=14
        )
        assert np.isclose(ant.wavelength, 0.02143, rtol=0.1)
        assert np.isclose(watt_to_decibel(ant.gain), g, rtol=0.1)


def test_parabolic_antenna_1():
    ant = ParabolicAntenna(
        name="test", circular_diameter=8, efficiency=0.5, frequency=7
    )
    assert np.isclose(watt_to_decibel(ant.gain), 52.4, rtol=0.1)


def test_square_horn_antenna():
    ant = SquareHornAntenna(
        name="test", cross_sect_diameter=0.07, efficiency=0.45, frequency=14
    )
    assert np.isclose(ant.wavelength, 0.02143, rtol=0.1)
    assert np.isclose(watt_to_decibel(ant.gain), 17.8, rtol=0.1)
    assert np.isclose(ant.half_beamwidth, 15.44, rtol=0.1)


def test_square_horn_antenna_1():
    ant = SquareHornAntenna(
        name="test", cross_sect_diameter=0.07, efficiency=0.45, frequency=12
    )
    assert np.isclose(watt_to_decibel(ant.gain), 16.47, rtol=0.1)
    assert np.isclose(ant.half_beamwidth, 18.0, rtol=0.1)


def test_pointing_loss():
    ant = Antenna(name="test", half_beamwidth=1)
    pointing_error = degrees(0.002)
    assert np.isclose(
        -watt_to_decibel(ant.pointing_loss(pointing_error)), 0.16, rtol=0.1
    )


def test_pointing_loss_1():
    ant = Antenna(name="test", half_beamwidth=2)
    pointing_error = degrees(0.005)
    assert np.isclose(
        -watt_to_decibel(ant.pointing_loss(pointing_error)), 0.246, rtol=0.1
    )
