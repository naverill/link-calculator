from link_calculator.constants import EARTH_RADIUS
from link_calculator.orbits.utils import (
    angle_sat_to_ground_station,
    angle_sat_to_gs_orbital_radius,
    slant_range,
)
from link_calculator.propagation.attenuation import free_space_loss_db, receive_power
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
)


def test_receive_power(
    transmit_power: float,
    transmit_loss: float,
    transmit_gain: float,
    distance: float,
    receive_gain: float,
    receive_loss: float,
    atmospheric_loss: float,
    wavelength: float = None,
    eff_aperture: float = None,
) -> None:
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
    print("Receive Power (dBW): ", watt_to_decibel(power))


def test_free_space_loss_orbit(elevation: float, orbit_radius: float, frequency: float):
    gamma = angle_sat_to_gs_orbital_radius(orbit_radius, elevation=elevation)
    spath = slant_range(orbit_radius, gamma)
    space_loss = free_space_loss_db(spath, frequency)
    print("Free Space Loss Orbit (dB): ", space_loss)


def test_free_space_loss(
    sat_lat: float,
    sat_long: float,
    gs_lat: float,
    gs_long: float,
    frequency: float,
    orbit_radius: float,
):
    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    spath = slant_range(orbit_radius, gamma)
    space_loss = free_space_loss_db(spath, frequency)
    print("Free Space Loss (dB): ", space_loss)


if __name__ == "__main__":
    trans_power = 9  # W
    trans_gain = decibel_to_watt(16)  # W
    trans_loss = decibel_to_watt(-3)  # W
    distance = 24500 * 1000  # m

    orbit_radius = 42164  # km
    elevation = 10  # deg
    receive_loss = decibel_to_watt(-2)  # W
    receive_gain = decibel_to_watt(57)  # W

    atmospheric_loss = decibel_to_watt(-9)  # W

    eff_aperture = None  # m^2
    wavelength = frequency_to_wavelength(11)  # m
    frequency = 10  # GHz

    sat_lat = 0
    sat_long = 9
    gs_lat = 32
    gs_long = -23
    test_receive_power(
        trans_power,
        trans_loss,
        trans_gain,
        distance,
        receive_loss,
        receive_gain,
        atmospheric_loss,
        wavelength=wavelength,
    )
    test_free_space_loss(sat_lat, sat_long, gs_lat, gs_long, frequency, orbit_radius)
