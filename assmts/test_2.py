from math import degrees, pi

import numpy as np

from link_calculator.components.antennas import (
    Amplifier,
    Antenna,
    ParabolicAntenna,
    SquareHornAntenna,
)
from link_calculator.components.communicators import GroundStation, Satellite
from link_calculator.constants import EARTH_RADIUS, SPEED_OF_LIGHT
from link_calculator.orbits.utils import (
    GeodeticCoordinate,
    Orbit,
    central_angle_orbital_radius,
    slant_range,
)
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
    wavelength_to_frequency,
)
from link_calculator.propagation.utils import rain_attenuation
from link_calculator.signal_processing.conversions import GHz_to_MHz, MHz_to_GHz
from link_calculator.signal_processing.modulation import (
    BinaryPhaseShiftKeying,
    MPhaseShiftKeying,
    QuadraturePhaseShiftKeying,
    Waveform,
)


def test_q1():
    """
    A satellite, with a slant range of 14000 km to an Earth station, radiates
    a power of 10 W at a frequency of 24 GHz from an antenna with a gain of 10
    dB. Find the power received by the Earth station if it has an antenna with
    a gain of 55 dB. The transmitter feeder loss is 4 dB, the receiver feeder
    loss is 2 dB and the atmospheric loss is assumed to be 7 dB.
    """
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
    assert np.isclose(watt_to_decibel(pow), -141, rtol=0.5)


def test_q2():
    """
    Calculate the free-space loss for a geostationary satellite at 13oE transmitting
    at a frequency of 13 GHz to an Earth station at 15oW and 16oN.
    """
    gs_lat = 0
    gs_long = 13
    sat_lat = 16
    sat_long = -15
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)
    orbital_radius = 42164
    orbit = Orbit(orbital_radius=orbital_radius)

    sat = Satellite(orbit=orbit)
    print(sat)
    gamma = point.central_angle(ss_point)
    sr = slant_range(42164, gamma)
    print(sr)
    # loss = free_space_loss(sr, frequency_to_wavelength(13))
    # assert np.isclose(watt_to_decibel(loss), -206.1, rtol=0.01)


def test_q3():
    """
    Calculate the gain of a 12 cm square pyramidal horn antenna with an efficiency
    of 70% transmitting at 16 GHz.
    """
    ant = SquareHornAntenna(
        name="test", cross_sect_diameter=0.12, efficiency=0.7, frequency=16
    )
    assert np.isclose(watt_to_decibel(ant.gain), 25.6, rtol=0.01)


def test_q4():
    """
    Calculate the gain of a parabolic reflector with a diameter of 12 m and an
    efficiency of 60% transmitting at 16 GHz.
    """
    ant = ParabolicAntenna(
        name="test", circular_diameter=12, efficiency=0.6, frequency=16
    )
    assert np.isclose(watt_to_decibel(ant.gain), 63.8, rtol=0.01)


def test_q5():
    """
    If a parabolic antenna, with a diameter of 3 m, has a half-power beamwidth
    of 0.3 degrees at a frequency of 25 GHz, calculate the half-power beamwidth,
    in degrees, for this antenna at a frequency of 10 GHz.
    """
    # k = (0.3 * pi / 180) * 3 / frequency_to_wavelength(25)
    theta = 1.3099 * (frequency_to_wavelength(10) / 3)
    beamwidth = theta * 180 / pi
    assert np.isclose(beamwidth, 0.750, rtol=0.75)


def test_q6():
    """
    A particular Ku band satellite is operated to stay within a 'box' so that
    it is no more than ±0.07° from its nominal geostationary orbital slot.
    What is the maximum sized parabolic antenna (in metres) that can be used
    in a ground station, without tracking capability, such that the antenna
    pointing loss is no more than 1 dB?

    Assume that the ground station is located at the nominal sub-satellite point,
    that the antenna is pointed optimally, and that the antenna’s shape factor (k)
    is 1.4. The operating frequencies are 14.5 GHz uplink and 12.0 GHz downlink.
    """
    ant = ParabolicAntenna(half_beamwidth=1)
    pointing_error = degrees(0.002)
    print(
        np.isclose(-watt_to_decibel(ant.pointing_loss(pointing_error)), 0.16, rtol=0.1)
    )
    """
    The maximum position error for the satellite of ±0.07° is with respect to the centre of the earth. At the Geostationary orbital radius of 42,164km, this is 42164 * 0.07 / 2π = ±52km

From the subsatellite point, the error becomes 2π * 52 / (42164-6378) = 0.082°

Re-arranging eqn 5-22 gives θb = θe/√(Lap/11.98), for Lap in dB

Combining this with eqn 5-14 gives D = k λ √(Lap/11.98) / θe = 1.4 * (3E8/14.5E9) * √(1/11.98) / (0.082/2π) = 5.81m
The correct answer is: 5.8
    """


def test_q7():
    """
    Calculate the maximum bit rate (in Mbit/s) for a digital signal that is transmitted over a channel with an RF bandwidth of 35 MHz using a digital modulation scheme that can transmit 4 bits/symbol. The transmitter and receiver use filters with a roll-off factor of 0.3.
    """
    bandwidth = 60
    carrier_to_noise = decibel_to_watt(7.75)
    bit_rate = 40  # bits/s

    mod = MPhaseShiftKeying(
        levels=4,
        bandwidth=bandwidth,
        bit_rate=bit_rate,
        carrier_to_noise=carrier_to_noise,
    )
    assert np.isclose(watt_to_decibel(mod.eb_no), 9.5, rtol=0.01)


def test_q8():
    """
    A satellite communications link has a bandwidth of 60 MHz and a C/N ratio of 7.75 dB. If data is transmitted using QPSK modulation, at a rate of 40 Mbit/s use the plots in the figure below to determine the BER for the link.
    """
    print(frequency_to_wavelength(14.5))
    """
    1x10-5
    """


def test_q9():
    """
    A communications channel with a bandwidth of 60 MHz, a filter roll-off factor of 0.25 and a C/N ratio of 12 dB is used to transmit data over a satellite link using a QPSK modulation scheme. What is the maximum bit rate and the bit error rate for this channel? If the modulation scheme is changed from QPSK to 8-PSK, what is the new maximum bit rate and bit error rate for the channel?
    """
    bandwidth = 60
    carrier_to_noise = decibel_to_watt(7.75)
    rolloff = 0.25
    carrier_to_noise = decibel_to_watt(12)  # bits/s

    M = 4
    bit_rate = np.log2(M) * bandwidth / (1 + rolloff)
    mod = MPhaseShiftKeying(
        levels=M,
        bandwidth=bandwidth,
        bit_rate=bit_rate,
        carrier_to_noise=carrier_to_noise,
    )
    assert np.isclose(watt_to_decibel(mod.eb_no), 10, rtol=0.01)

    M = 8
    bit_rate = np.log2(M) * bandwidth / (1 + rolloff)
    mod = MPhaseShiftKeying(
        levels=8, bandwidth=bandwidth, bit_rate=144, carrier_to_noise=carrier_to_noise
    )
    assert np.isclose(watt_to_decibel(mod.eb_no), 8.2, rtol=0.01)


def test_q10():
    """
    A communications channel with a bandwidth of 30 MHz and a filter roll-off factor of 0.25 is to be established over a satellite link. A convolutional channel coder will be used to prepare the data for transmission over the satellite channel and an 8-PSK modulation scheme will be used to transmit information over the channel. If no channel coding is used, the communications channel has a C/N ratio of 15 dB. For a code rate of 7/8 the convolutional coder has a coding gain of 2 dB, for a code rate of 3/4 the coding gain is 3 dB and for a code rate of 1/2 the coding gain is 4 dB.
    """
    pass


def test_q11():
    """
    In a satellite system, an Earth station with a 60 cm parabolic dish is used to receive a broadcast television signal from a Geostationary satellite located at 150o E. The efficiency of the Earth station antenna is 60 % and the feeder loss is 1 dB. The satellite antenna has a gain of 25 dB and the feeder loss is 0.5 dB. For a frequency of 12.75 GHz, calculate the satellite transmitter power (in Watts) that is needed to produce a receiver power, in the Earth station, of -140 dBW at an elevation angle of 20o. Assume that the atmospheric loss is 5 dB.
    """
    pass
    radius = 42164
    gamma = central_angle_orbital_radius(radius, elevation=20)
    sr = slant_range(radius, gamma)
    print(sr)
    receive = ParabolicAntenna(
        frequency=12.75,
        circular_diameter=0.6,
        efficiency=0.6,
    )
    transmit = Antenna(name="test", frequency=12.75, gain=decibel_to_watt(25), loss=0.5)
    print(receive.effective_aperture)
    exit()
    pow = receive.receive_power(transmit, 14000, decibel_to_watt(7))
    print(watt_to_decibel(pow))
    """
    The wavelength of the transmitted signal is 0.0235 m

    Since the satellite is geostationary, rs = 42,164 km
    Using equation 2-31, the central angle is 61.8 degrees
    Using equation 2-23 the slant range is 39,554 km
    Using equation 4-17 the free space loss (LFS) is 206.5 dB
    Using equation 5-13 the gain of the Earth station antenna is 35.9 dB

    Then rearranging equation 4-13 to find Pt when Pr is given:

    Pt = Pr-Gt+Lt+LFS+LA-Gr+Lr = -140-25+0.5+206.5+5-35.9+1 = 12.1 dBW or 16.2 W
    """


def test_q12():
    """
    In a satellite system, handheld terminals similar in size to a mobile phone are to be used to communicate with a Geostationary satellite located at 110o E. The antenna in the handheld terminal has a gain of 2 dB and a feeder loss of 0.1 dB. The satellite transmitter power is 20W and feeder loss is 0.5 dB. For a frequency of 1.55 GHz, calculate the diameter of a parabolic antenna, mounted on the satellite, that is needed to produce a receiver power, in the handheld terminal, of -130 dBW at an elevation angle of 10o. Assume the parabolic antenna has an efficiency of 65%.
    """
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
    transmit = Antenna(frequency=12.75, gain=decibel_to_watt(25), loss=0.5)
    print(receive.effective_aperture)
    print(transmit)
    """
    The satellite transmitter power is 10*log10(20) = 13 dB

    The wavelength of the transmitted signal is 0.1935 m

    Since the satellite is geostationary, rs = 42,164 km


    Using equation 2-31, the central angle is 71.4 degrees

    Using equation 2-23 the slant range is 40,586 km

    Using equation 4-17 the free space loss (LFS) is 188.4 dB

    Then rearranging equation 4-13 to find Gt when Pr is given:

    Gt = Pr-Pt+Lt+LFS-Gr+Lr = -130-13+0.5+188.4-2+0.1 = 44 dB or 25,119

    Then using a rearranged version of equation 5-13 the required diameter of the parabolic antenna is 12.1 m.
    """
