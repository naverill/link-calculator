from math import isclose, radians, sqrt

import numpy as np

from link_calculator.constants import (
    EARTH_MASS,
    EARTH_POLAR_RADIUS,
    EARTH_RADIUS,
    GRAVITATIONAL_CONSTANT,
    PLUTO_MASS,
    SIDEREAL_DAY_S,
    SUN_MU,
)
from link_calculator.coordinates.orbits import (
    CircularOrbit,
    EllipticalOrbit,
    HyperbolicOrbit,
    Orbit,
    ParabolicOrbit,
)
from link_calculator.coordinates.utils import central_angle_radius


def test_circular_period():
    ht = [250, 500, 1000, 10000]  # height
    pd = [5370, 5677, 6307, 20860]  # period

    for h, T in zip(ht, pd):
        coord = CircularOrbit(semimajor_axis=h + EARTH_RADIUS)
        assert isclose(coord.period, T, rel_tol=0.5)


def test_circular_period_1():
    h = 23200
    coord = CircularOrbit(semimajor_axis=h + EARTH_RADIUS)
    assert isclose(coord.period, 50625, rel_tol=0.5)


def test_circular_velocity():
    h = 150 * 1.852
    coord = CircularOrbit(radius=h + EARTH_RADIUS)
    assert isclose(coord.velocity, 7.739, rel_tol=0.5)
    assert isclose(coord.period, 5404, rel_tol=0.5)


def test_elliptical_true_anomaly():
    orbit = EllipticalOrbit(
        periapsis_radius=6500,
        apoapsis_radius=60000,
        radius=EARTH_RADIUS + 500,
    )
    assert np.isclose(orbit.eccentricity, 0.8045, rtol=0.01)
    assert np.isclose(orbit.true_anomaly, 28.755, rtol=0.01)


def test_elliptical_transfer_perigee_radius():
    """
    Design a transfer ellipse from Earth at a heliocentric position of r = 1.00 AU
    and a longitude of 41.26° to Pluto at r = 39.5574 AU and a longitude of 194.66°.
    Place the line of apsides at a longitude of 25°.
    """
    e = EllipticalOrbit.transfer_eccentricity(
        radius1=1.49598e8, true_anomaly1=16.26, radius2=5.9177e9, true_anomaly2=169.66
    )
    assert np.isclose(e, 0.9670, rtol=0.01)
    mu = GRAVITATIONAL_CONSTANT * (EARTH_MASS + PLUTO_MASS)
    orbit = EllipticalOrbit(mu=mu, eccentricity=e, radius=1.49598e8, true_anomaly=16.26)
    assert np.isclose(orbit.periapsis_radius, 1.4666e8, rtol=0.01)


def test_hyperbolic_velocity():
    orbit = Orbit(
        radius=1500 + EARTH_RADIUS, velocity=10.7654, flight_path_angle=23.174
    )
    assert np.isclose(orbit.specific_energy, 7.351169, rtol=0.01)
    assert np.isclose(orbit.semimajor_axis, -27111.36, rtol=0.01)
    assert np.isclose(orbit.specific_momentum, 77968.2, rtol=0.01)
    assert np.isclose(orbit.eccentricity, 1.250, rtol=0.01)


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
    radius = 500 + EARTH_POLAR_RADIUS
    coord = CircularOrbit(semimajor_axis=radius)
    orbital_period = coord.period
    assert isclose(orbital_period, 5713, rel_tol=0.1)

    orbits_per_day = SIDEREAL_DAY_S / orbital_period
    assert isclose(orbits_per_day, 15.1, rel_tol=0.1)
    deg_shift_per_orbit = 360 / orbits_per_day

    gamma = central_angle_radius(radius)
    assert isclose(gamma, 21.7, rel_tol=0.1)

    total_swath = gamma * 2
    assert total_swath > deg_shift_per_orbit
