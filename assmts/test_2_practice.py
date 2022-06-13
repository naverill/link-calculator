import numpy as np

from link_calculator.components.antennas import Antenna, ParabolicAntenna
from link_calculator.components.groundstation import GroundStation
from link_calculator.components.satellite import Satellite
from link_calculator.constants import EARTH_RADIUS, SPEED_OF_LIGHT
from link_calculator.link_budget import Link
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


def test_q3():
    """
    The constellation is instead operated at an altitude of 550 km and allows the signals to
    be relayed through more than one satellite. The maximum distance between satellites is
    1000 km. How many satellite-to-satellite ‘hops’ can the network support while still
    meeting the maximum delay time constraint?
    """
    orbital_radius = 550 + EARTH_RADIUS

    gamma = central_angle_orbital_radius(orbital_radius, elevation=20)
    sr = slant_range(orbital_radius, gamma)
    time_to_sat = sr * 1000 / SPEED_OF_LIGHT * 1000
    time_between_sat = 1000 * 1000 / SPEED_OF_LIGHT * 1000 + 5
    m = (50 - 2 * time_to_sat) / time_between_sat
    assert np.isclose(np.floor(m), 4, rtol=0.01)


def test_q4():
    """
    An Earth station is located at 94oW  and 48oN and a satellite has an orbital height
    of 22500 km. If the sub-satellite point of the satellite is at 96oW and 22oN,
    calculate the free space loss, in dB, between the Earth station and the satellite
    at a frequency of 24 GHz.
    """
    gs_long = -94
    gs_lat = 48
    sat_long = -96
    sat_lat = 22
    orbital_radius = 22500 + EARTH_RADIUS  # km

    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    orbit = Orbit(orbital_radius=orbital_radius)
    sat = Satellite(name="test", ground_coordinate=ss_point, orbit=orbit)
    gs = GroundStation(name="test", ground_coordinate=point)

    # frequency = 24  # GHz
    # wavelength = frequency_to_wavelength(frequency)
    # gamma = point.central_angle(ss_point)
    # sr = slant_range(orbital_radius, gamma)

    link = Link(transmit=gs, receive=sat)
    assert np.isclose(watt_to_decibel(link.path_loss), -207.4, rtol=0.01)


def test_q5():
    """
    A communications channel with a bandwidth of 30 MHz and a filter roll-off factor of 0.5
    is used to transmit data over a satellite link using a BPSK modulation scheme. What
    is the maximum bit rate for this channel? If the modulation scheme is changed from
    BPSK to QPSK, what is the new maximum bit rate?
    """
    rolloff = 0.5
    bandwidth = MHz_to_GHz(30)

    mod = BinaryPhaseShiftKeying(
        bandwidth=bandwidth,
        rolloff_rate=rolloff,
    )
    assert np.isclose(mod.bit_rate, 0.02, rtol=0.01)
    modq = QuadraturePhaseShiftKeying(
        bandwidth=bandwidth,
        rolloff_rate=rolloff,
    )
    assert np.isclose(modq.bit_rate, 0.04, rtol=0.01)


def test_q6():
    """
    A satellite has an equatorial orbit with an orbital height of 550 km. For an
    Earth station located on the equator, determine the period of time that the
    satellite will have an elevation angle of greater than 5o. Assume that the
    rotation of the Earth during this time is negligible.
    """
    orbital_radius = 550 + EARTH_RADIUS
    elevation = 5
    gamma = central_angle_orbital_radius(orbital_radius, elevation=elevation)

    vis = gamma * 2
    total_orbit_per = vis / 360

    assert np.isclose(gamma, 18.5, rtol=0.01)
    assert np.isclose(vis, 37, rtol=0.01)
    coord = Orbit(orbital_radius)
    t = coord.period()
    assert np.isclose(t, 5736, rtol=0.01)
    time_visible = t * total_orbit_per
    assert np.isclose(time_visible, 589.61, rtol=0.01)


def test_q7():
    """
    A satellite communications link has a bandwidth of 30 MHz and a C/N ratio of
    15.5 dB. If data is transmitted using 8-PSK modulation, at a rate of 60 Mbit/s,
    use the plots in the figure below to determine the BER for the link.
    """
    # bandwidth = MHz_to_GHz(30)
    # carrier_to_noise = decibel_to_watt(15.5)
    # bit_rate = 0.06  # bits/s

    # mod = MPhaseShiftKeying(
    #     levels=8,
    #     bandwidth=bandwidth,
    #     bit_rate=bit_rate,
    #     carrier_to_noise=carrier_to_noise,
    # )
    # assert np.isclose(watt_to_decibel(mod.eb_no), 8.8, rtol=0.01)
    pass


def test_q8():
    """
    A communications channel with a bandwidth of 60 MHz and a filter roll-off
    factor of 0.2 is to be established over a satellite link. A convolutional
    channel coder will be used to prepare the data for transmission over the
    satellite channel and an 8-PSK modulation scheme will be used to transmit
    information over the channel.  For a code rate of 7/8 the convolutional
    coder has a coding gain of 2 dB, for a code rate of 3/4 the coding gain
    is 3 dB and for a code rate of 1/2 the coding gain is 4 dB. The channel
    is required to provide a data rate of 100 Mbits/s while maintaining a
    bit error rate of less than 1x10-7. Find the minimum carrier-to-noise ratio
    (C/N) for the satellite link that will be required to provide this service.
    """
    bandwidth = 60
    roll_off = 0.2
    min_eb_no = 14.75

    mod = MPhaseShiftKeying(levels=8, bandwidth=bandwidth, rolloff_rate=roll_off)
    assert np.isclose(mod.bit_rate, 150, rtol=0.01)
    c_n = min_eb_no - watt_to_decibel(bandwidth / mod.bit_rate) - 3
    assert np.isclose(c_n, 15.75, rtol=0.01)
