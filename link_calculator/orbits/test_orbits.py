from math import isclose, radians

from link_calculator.constants import EARTH_RADIUS
from link_calculator.orbits.utils import (
    angle_sat_to_ground_station,
    angle_sat_to_gs_orbital_radius,
    azimuth_intermediate,
    elevation_angle,
    percentage_of_coverage,
    period,
    slant_range,
)


def test_period():
    ht = [250, 500, 1000, 10000]  # height
    pd = [5370, 5677, 6307, 20860]  # period

    for h, T in zip(ht, pd):
        assert isclose(period(h + EARTH_RADIUS), T, rel_tol=0.5)


def test_percentage_of_coverage():
    height = [250, 500, 1000, 10000, 10000]
    angle = [0, 0, 0, 0, 5]
    per = [1.89, 3.63, 6.78, 30.53, 26.66]

    for h, a, p in zip(height, angle, per):
        gamma = angle_sat_to_gs_orbital_radius(h + EARTH_RADIUS, elevation=a)
        assert isclose(percentage_of_coverage(gamma), p, rel_tol=0.5)


def test_azimuth_intermediate_NE():
    # nothern hemisphere, sat to the east
    gs_lat = 30
    gs_long = -120
    sat_long = -90

    assert isclose(azimuth_intermediate(gs_lat, gs_long, sat_long), 49.11, rel_tol=0.1)


def test_azimuth_intermediate_NW():
    # northern hemisphere, sat the to west
    gs_lat = 52
    gs_long = 0
    sat_long = 66
    from math import degrees

    assert isclose(azimuth_intermediate(gs_lat, gs_long, sat_long), 70.7, rel_tol=0.1)


def test_azimuth_intermediate_SW():
    # southern hemisphere, sat to the west
    gs_lat = -30
    gs_long = 360 - 30
    sat_long = 30

    assert isclose(azimuth_intermediate(gs_lat, gs_long, sat_long), 73.9, rel_tol=0.1)


def test_azimuth_intermediate_SE():
    # northern hemisphere, sat the to west
    gs_lat = 52
    gs_long = 0
    sat_long = 66
    from math import degrees

    assert isclose(azimuth_intermediate(gs_lat, gs_long, sat_long), 70.7, rel_tol=0.1)


def test_elevation_angle():
    gs_lat = 30
    gs_long = -120
    sat_long = -90

    # Geo-stationary satellite
    sat_lat = 0
    orbital_radius = 42164

    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)

    assert isclose(elevation_angle(orbital_radius, gamma), 42.15, rel_tol=0.1)


def test_elevation_angle_2():
    gs_lat = -30
    gs_long = -30
    sat_long = 30
    sat_lat = 0
    orbital_radius = 42164

    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    assert isclose(elevation_angle(orbital_radius, gamma), 17.36, rel_tol=0.1)


def test_slant_range():
    gs_lat = 30
    gs_long = -120
    sat_long = -90

    # Geo-stationary satellite
    sat_lat = 0
    orbital_radius = 42164

    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    assert isclose(slant_range(orbital_radius, gamma), 37618, rel_tol=0.5)


def test_slant_range_2():
    gs_lat = -30
    gs_long = -30
    sat_long = 30

    sat_lat = 0
    orbital_radius = 42164

    gamma = angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
    assert isclose(slant_range(orbital_radius, gamma), 39819, rel_tol=0.1)
