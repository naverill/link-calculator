from link_calculator.components.antennas import Antenna, ParabolicAntenna
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


def q3():
    orbital_radius = 550 + EARTH_RADIUS

    gamma = central_angle_orbital_radius(orbital_radius, elevation=20)
    sr = slant_range(orbital_radius, gamma)
    print(gamma, sr)
    time_to_sat = sr * 1000 / SPEED_OF_LIGHT * 1000
    print(time_to_sat)
    time_between_sat = 1000 * 1000 / SPEED_OF_LIGHT * 1000 + 5
    print(time_between_sat)
    m = (50 - 2 * time_to_sat) / time_between_sat
    print(m)


def q4():
    gs_long = -94
    gs_lat = 48
    sat_long = -96
    sat_lat = 22
    orbital_radius = 22500 + EARTH_RADIUS  # km

    frequency = 24  # GHz
    wavelength = frequency_to_wavelength(frequency)
    gamma = central_angle(gs_lat, gs_long, sat_lat, sat_long)
    sr = slant_range(orbital_radius, gamma)

    loss = free_space_loss(sr, wavelength)
    print("q4", watt_to_decibel(loss))


def q5():
    rolloff = 0.5
    bandwidth = MHz_to_GHz(30)

    mod = BinaryPhaseShiftKeying(
        bandwidth=bandwidth,
        rolloff_rate=rolloff,
    )
    print(mod.bit_rate)
    modq = QuadraturePhaseShiftKeying(
        bandwidth=bandwidth,
        rolloff_rate=rolloff,
    )
    print(modq.bit_rate)


def q6():
    orbital_radius = 550 + EARTH_RADIUS
    elevation = 5
    gamma = central_angle_orbital_radius(orbital_radius, elevation=elevation)

    vis = gamma * 2
    total_orbit_per = vis / 360

    print("v", vis)
    print("gamma", gamma)
    t = period(orbital_radius)
    print("T", t)
    time_visible = t * total_orbit_per
    print("visible", time_visible)


def q7():
    bandwidth = 30
    carrier_to_noise = decibel_to_watt(15.5)
    bit_rate = 60  # bits/s

    mod = MPhaseShiftKeying(
        levels=8,
        bandwidth=bandwidth,
        bit_rate=bit_rate,
        carrier_to_noise=carrier_to_noise,
    )
    print(watt_to_decibel(mod.eb_no))


def q8():
    bandwidth = 60
    roll_off = 0.2
    min_eb_no = 14.75

    mod = MPhaseShiftKeying(levels=8, bandwidth=bandwidth, rolloff_rate=roll_off)
    print(mod.bit_rate)
    c_n = min_eb_no - watt_to_decibel(bandwidth / mod.bit_rate) - 3
    print(c_n)


if __name__ == "__main__":
    q8()
