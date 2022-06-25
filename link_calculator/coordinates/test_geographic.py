from math import isclose, radians, sqrt

import numpy as np

from link_calculator.coordinates.geographic import GeodeticCoordinate


def test_central_angle():
    gs_long = -17
    gs_lat = 40
    sat_long = 5
    sat_lat = 0
    point = GeodeticCoordinate(gs_lat, gs_long)
    ss_point = GeodeticCoordinate(sat_lat, sat_long)
    assert isclose(point.central_angle(ss_point), 44.7, rel_tol=0.01)
