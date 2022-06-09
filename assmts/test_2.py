from math import degrees, pi

import numpy as np

from link_calculator.components.antennas import (
    Antenna,
    ParabolicAntenna,
    SquareHornAntenna,
)
from link_calculator.components.groundstation import GroundStation
from link_calculator.components.satellite import Satellite
from link_calculator.constants import EARTH_RADIUS, SPEED_OF_LIGHT
from link_calculator.orbits.utils import (
    central_angle,
    central_angle_orbital_radius,
    period,
    slant_range,
)
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
    wavelength_to_frequency,
)
from link_calculator.propagation.utils import free_space_loss, rain_attenuation
from link_calculator.signal_processing.conversions import GHz_to_MHz, MHz_to_GHz
from link_calculator.signal_processing.modulation import (
    BinaryPhaseShiftKeying,
    MPhaseShiftKeying,
    QuadraturePhaseShiftKeying,
    Waveform,
)


def q1():
    transmit = Antenna(
        name="test",
        power=10,
        frequency=24,
        gain=decibel_to_watt(10),
        loss=decibel_to_watt(4),
    )
    receive = Antenna(
        name="test", frequency=24, gain=decibel_to_watt(55), loss=decibel_to_watt(2)
    )
    pow = receive.receive_power(transmit, 14000, decibel_to_watt(7))
    print(watt_to_decibel(pow))


def q2():
    gamma = central_angle(0, 13, 16, -15)
    sr = slant_range(42164, gamma)
    loss = free_space_loss(sr, 13)
    print(watt_to_decibel(loss))


def q3():
    ant = SquareHornAntenna(
        name="test", cross_sect_diameter=0.12, efficiency=0.7, frequency=16
    )
    print(watt_to_decibel(ant.gain))


def q4():
    ant = ParabolicAntenna(
        name="test", circular_diameter=12, efficiency=0.6, frequency=16
    )
    print(watt_to_decibel(ant.gain))


def q5():
    k = (0.3 * pi / 180) * 3 / frequency_to_wavelength(25)
    print(k)

    theta = 1.3099 * (frequency_to_wavelength(10) / 3)
    print(theta * 180 / pi)


def q6():
    ant = ParabolicAntenna(name="test", half_beamwidth=1)
    pointing_error = degrees(0.002)
    assert np.isclose(
        -watt_to_decibel(ant.pointing_loss(pointing_error)), 0.16, rtol=0.1
    )


def q7():
    print(frequency_to_wavelength(14.5))


def q8():
    bandwidth = 60
    carrier_to_noise = decibel_to_watt(7.75)
    bit_rate = 40  # bits/s

    mod = MPhaseShiftKeying(
        levels=4,
        bandwidth=bandwidth,
        bit_rate=bit_rate,
        carrier_to_noise=carrier_to_noise,
    )
    print(watt_to_decibel(mod.eb_no))


def q9():
    bandwidth = 60
    carrier_to_noise = decibel_to_watt(7.75)
    # rolloff = 0.25
    carrier_to_noise = decibel_to_watt(12)  # bits/s

    mod = MPhaseShiftKeying(
        levels=4, bandwidth=bandwidth, bit_rate=96, carrier_to_noise=carrier_to_noise
    )
    print(watt_to_decibel(mod.eb_no))

    mod = MPhaseShiftKeying(
        levels=8, bandwidth=bandwidth, bit_rate=144, carrier_to_noise=carrier_to_noise
    )
    print(watt_to_decibel(mod.eb_no))


def q11():
    radius = 42164
    gamma = central_angle_orbital_radius(radius, elevation=20)
    sr = slant_range(radius, gamma)
    print(sr)
    receive = ParabolicAntenna(
        name="test",
        frequency=12.75,
        circular_diameter=0.6,
        efficiency=0.6,
    )
    transmit = Antenna(name="test", frequency=12.75, gain=decibel_to_watt(25), loss=0.5)
    print(receive.effective_aperture)
    exit()
    pow = receive.receive_power(transmit, 14000, decibel_to_watt(7))
    print(watt_to_decibel(pow))


def q12():
    radius = 42164
    gamma = central_angle_orbital_radius(radius, elevation=10)
    print(gamma)
    sr = slant_range(radius, gamma)
    print(sr)
    receive = ParabolicAntenna(
        name="test",
        frequency=12.75,
        circular_diameter=0.6,
        efficiency=0.6,
    )
    transmit = Antenna(name="test", frequency=12.75, gain=decibel_to_watt(25), loss=0.5)
    print(receive.effective_aperture)
    print(transmit)


if __name__ == "__main__":
    q12()
