from math import isclose, radians, sqrt

import numpy as np

from link_calculator.constants import EARTH_POLAR_RADIUS, EARTH_RADIUS, SIDEREAL_DAY_S
from link_calculator.coordinates.geographic import GeodeticCoordinate
from link_calculator.coordinates.utils import (
    azimuth_intermediate,
    central_angle_radius,
    elevation_angle,
    percentage_of_coverage,
    slant_range,
)


def test_percentage_of_coverage():
    height = [250, 500, 1000, 10000, 10000]
    angle = [0, 0, 0, 0, 5]
    per = [1.89, 3.63, 6.78, 30.53, 26.66]

    for h, a, p in zip(height, angle, per):
        gamma = central_angle_radius(h + EARTH_RADIUS, elevation=a)
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


def test_azimuth_intermediate_NE_():
    # northern hemisphere, sat the to west
    gs_lat = 52
    gs_long = 0
    sat_long = 66
    from math import degrees

    assert isclose(azimuth_intermediate(gs_lat, gs_long, sat_long), 70.7, rel_tol=0.1)


def test_azimuth_intermediate_SE():
    #  southern hemisphere, sat to the east
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    assert isclose(azimuth_intermediate(gs_lat, gs_long, sat_long), 32.2, rel_tol=0.1)


def test_elevation_angle():
    gs_lat = 30
    gs_long = -120
    sat_long = -90
    # Geo-stationary satellite
    sat_lat = 0
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)
    radius = 42164

    gamma = point.central_angle(ss_point)

    assert isclose(elevation_angle(radius, gamma), 42.15, rel_tol=0.1)


def test_elevation_angle_1():
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    # Geo-stationary satellite
    sat_lat = 0
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)
    radius = 42164

    gamma = point.central_angle(ss_point)

    assert isclose(elevation_angle(radius, gamma), 38.4, rel_tol=0.1)


def test_elevation_angle_2():
    gs_lat = -30
    gs_long = -30
    sat_long = 30
    sat_lat = 0
    radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)
    assert isclose(elevation_angle(radius, gamma), 17.36, rel_tol=0.1)


def test_slant_range():
    gs_lat = 30
    gs_long = -120
    sat_long = -90

    # Geo-stationary satellite
    sat_lat = 0
    radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)
    assert isclose(slant_range(radius, gamma), 37618, rel_tol=0.5)


def test_slant_range_1():
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    # Geo-stationary satellite
    sat_lat = 0
    radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)

    assert isclose(slant_range(radius, gamma), 37901, rel_tol=0.5)


def test_slant_range_2():
    gs_lat = -30
    gs_long = -30
    sat_long = 30

    sat_lat = 0
    radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)
    assert isclose(slant_range(radius, gamma), 39819, rel_tol=0.1)


def test_central_angle_radius():
    radius = 2500 + EARTH_RADIUS
    elevation_angle = 10

    assert isclose(
        central_angle_radius(radius, elevation=elevation_angle),
        35.0,
        rel_tol=0.1,
    )


def test_percentage_coverage():
    radius = 2500 + EARTH_RADIUS
    elevation_angle = 10

    gamma = central_angle_radius(radius, elevation=elevation_angle)
    assert isclose(percentage_of_coverage(gamma), 9, rel_tol=0.1)
