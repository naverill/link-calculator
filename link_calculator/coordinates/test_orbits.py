from math import isclose, radians

from link_calculator.constants import EARTH_POLAR_RADIUS, EARTH_RADIUS, SIDEREAL_DAY_S
from link_calculator.geodeitc import GeodeticCoordinate
from link_calculator.orbits.utils import (
    CircularOrbit,
    EllipticalOrbit,
    HyperbolicOrbit,
    Orbit,
    ParabolicPrbit,
    azimuth_intermediate,
    central_angle_orbital_radius,
    elevation_angle,
    percentage_of_coverage,
    slant_range,
)


def test_circular_period():
    ht = [250, 500, 1000, 10000]  # height
    pd = [5370, 5677, 6307, 20860]  # period

    for h, T in zip(ht, pd):
        coord = CircularOrbit(semi_major_axis=h + EARTH_RADIUS)
        assert isclose(coord.period, T, rel_tol=0.5)


def test_circular_period_1():
    h = 23200
    coord = CircularOrbit(semi_major_axis=h + EARTH_RADIUS)
    assert isclose(coord.period, 50625, rel_tol=0.5)


def test_circular_velocity():
    h = 150 * 1.852
    coord = CircularOrbit(orbital_radius=h + EARTH_RADIUS)
    assert isclose(coord.velocity, 7.739, rel_tol=0.5)
    assert isclose(coord.period, 5404, rel_tol=0.5)


def test_percentage_of_coverage():
    height = [250, 500, 1000, 10000, 10000]
    angle = [0, 0, 0, 0, 5]
    per = [1.89, 3.63, 6.78, 30.53, 26.66]

    for h, a, p in zip(height, angle, per):
        gamma = central_angle_orbital_radius(h + EARTH_RADIUS, elevation=a)
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
    orbital_radius = 42164

    gamma = point.central_angle(ss_point)

    assert isclose(elevation_angle(orbital_radius, gamma), 42.15, rel_tol=0.1)


def test_elevation_angle_1():
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    # Geo-stationary satellite
    sat_lat = 0
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)
    orbital_radius = 42164

    gamma = point.central_angle(ss_point)

    assert isclose(elevation_angle(orbital_radius, gamma), 38.4, rel_tol=0.1)


def test_elevation_angle_2():
    gs_lat = -30
    gs_long = -30
    sat_long = 30
    sat_lat = 0
    orbital_radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)
    assert isclose(elevation_angle(orbital_radius, gamma), 17.36, rel_tol=0.1)


def test_slant_range():
    gs_lat = 30
    gs_long = -120
    sat_long = -90

    # Geo-stationary satellite
    sat_lat = 0
    orbital_radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)
    assert isclose(slant_range(orbital_radius, gamma), 37618, rel_tol=0.5)


def test_slant_range_1():
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    # Geo-stationary satellite
    sat_lat = 0
    orbital_radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)

    assert isclose(slant_range(orbital_radius, gamma), 37901, rel_tol=0.5)


def test_slant_range_2():
    gs_lat = -30
    gs_long = -30
    sat_long = 30

    sat_lat = 0
    orbital_radius = 42164
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)

    gamma = point.central_angle(ss_point)
    assert isclose(slant_range(orbital_radius, gamma), 39819, rel_tol=0.1)


def test_central_angle():
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    sat_lat = 0
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)
    assert isclose(point.central_angle(ss_point), 44.7, rel_tol=0.01)


def test_central_angle_orbital_radius():
    orbital_radius = 2500 + EARTH_RADIUS
    elevation_angle = 10

    assert isclose(
        central_angle_orbital_radius(orbital_radius, elevation=elevation_angle),
        35.0,
        rel_tol=0.1,
    )


def test_percentage_coverage():
    orbital_radius = 2500 + EARTH_RADIUS
    elevation_angle = 10

    gamma = central_angle_orbital_radius(orbital_radius, elevation=elevation_angle)
    assert isclose(percentage_of_coverage(gamma), 9, rel_tol=0.1)


def test_polar_coverage():
    """
    r_e= 6357 km (polar);  r_s = r_e+h = 6,857 km

    calculating the period of the orbit and letting μ = 390000 km3/s2,  the
    orbital period of the satellite is 5,713 seconds.

    A sidereal day is 86,164.1 seconds so the satellite will complete
    15.1 orbits in the time it takes for the Earth to rotate around
    its axis once. This means that at each pass, the point at which
    the satellite crosses the equator will move by 360/15.1=23.9
    degrees of longitude. For the satellite to image the entire earth,
    each swathe captured by the camera must overlap the preceding swathe.

    At the equator, the east and west extent of the swathe is equal to
    the central angle for the lowest elevation that is in view, so for
    0° elevation, we use eqn 2-28  which gives a central angle of 21.7°.
    This is on each side of the nadir point, so the total swathe is 43.4°
    wide, well over the angular distance between swathes. Therefore, the
    swathes overlap and so a camera mounted on the satellite can capture
    images of the whole earth in a single day.

    """
    orbital_radius = 500 + EARTH_POLAR_RADIUS
    coord = Orbit(semi_major_axis=orbital_radius)
    orbital_period = coord.period()
    assert isclose(orbital_period, 5713, rel_tol=0.1)

    orbits_per_day = SIDEREAL_DAY_S / orbital_period
    assert isclose(orbits_per_day, 15.1, rel_tol=0.1)
    deg_shift_per_orbit = 360 / orbits_per_day

    gamma = central_angle_orbital_radius(orbital_radius)
    assert isclose(gamma, 21.7, rel_tol=0.1)

    total_swath = gamma * 2
    assert total_swath > deg_shift_per_orbit
