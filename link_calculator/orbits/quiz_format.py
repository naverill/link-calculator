from constants import EARTH_RADIUS
from utils import (
    angle_sat_to_ground_station,
    angle_sat_to_gs_orbital_radius,
    azimuth_intermediate,
    elevation_angle,
    percentage_of_coverage_gamma,
    period,
    slant_range,
)


def test_period(orbital_radius):
    period = period(orbital_radius)
    print("Period (s)", period)


def test_azimuth(gs_lat, gs_long, sat_long):
    az = azimuth_intermediate(gs_lat, gs_long, sat_long)
    print("Intermediate (deg):", az)


def test_elevation(gs_lat, gs_long, sat_lat, sat_long, orbital_radius):
    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    el = elevation_angle(orbital_radius, gamma)
    print("Elevation (deg)", el)


def test_slant_range(gs_lat, gs_long, sat_lat, sat_long, orbital_radius):
    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    srange = slant_range(orbital_radius, gamma)
    print("Slant Range (km)", srange)


def test_gamma(gs_lat, gs_long, sat_lat, sat_long):
    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    print("Gamma (deg)", gamma)


def test_gamma_orbital_radius(orbital_radius, min_angle):
    gamma = angle_sat_to_gs_orbital_radius(orbital_radius, min_angle=min_angle)
    print("Gamma (radius, deg)", gamma)


def test_percent_coverage(orbital_radius, min_angle):
    gamma = angle_sat_to_gs_orbital_radius(orbital_radius, min_angle=min_angle)
    per = percentage_of_coverage_gamma(gamma)
    print("Percent Coverage", per)


if __name__ == "__main__":
    # Lat N-S
    # Long E-W
    gs_lat = -32
    gs_long = 149
    sat_lat = -35
    sat_long = 135

    gs_lat = -32
    gs_long = 149
    sat_lat = -35
    sat_long = 135

    # HEIGHT ABOVE SURFACE + EARTH_RADIUS
    orbital_radius = 1414 + EARTH_RADIUS
    print()
    # orbital_radius = 42164
    min_angle = 10

    test_gamma(gs_lat, gs_long, sat_lat, sat_long)
    test_period(orbital_radius)
    test_azimuth(gs_lat, gs_long, sat_long)
    test_elevation(gs_lat, gs_long, sat_lat, sat_long, orbital_radius)
    test_slant_range(gs_lat, gs_long, sat_lat, sat_long, orbital_radius)
    test_gamma_orbital_radius(orbital_radius, min_angle)
    test_percent_coverage(orbital_radius, min_angle)
