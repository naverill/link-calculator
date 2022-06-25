from math import acos, atan, cos, degrees, pi, radians, sin, sqrt, tan

import numpy as np
import pandas as pd

from link_calculator.constants import EARTH_MU, EARTH_RADIUS


def central_angle_radius(
    orbital_radius: float, planet_radius: float = EARTH_RADIUS, elevation: float = 0
):
    """
    Calculate angle gamma at the centre of the ground, between the Earth
    station and the satellite, given the orbital radius of the satellite

    Parameters
    ---------
        orbital_radius (float, km): distance from the centre of mass to the satellite
        planet_radius (float, km, optional): radius of the planet
        elevation (float, deg): the angle of elevation over the horizon

    Returns
    ------
        gamma (float, deg): angle between satellite and ground station
    """
    elevation_rad = radians(elevation)
    gamma = acos((planet_radius * cos(elevation_rad)) / orbital_radius) - elevation_rad
    return degrees(gamma)


def slant_range(
    orbital_radius: float, central_angle: float, planet_radius: float = EARTH_RADIUS
) -> float:
    """
    Calculate the slant range from the ground station to the satellite

    Parameters
    ----------
        orbital_radius (float, km): distance from the centre of mass to the satellite
        gamma (float, deg): central_angle; angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        slant_range (float, km): the distance from the ground station to the satellite

    """
    return sqrt(
        planet_radius**2
        + orbital_radius**2
        - 2 * planet_radius * orbital_radius * cos(radians(central_angle))
    )


def elevation_angle(
    orbital_radius: float, central_angle: float, planet_radius: float = EARTH_RADIUS
) -> float:
    """
    Calculate the elevation angle from the ground station to the satellite

    Parameters
    ----------
        orbital_radius (float, km): distance from the centre of mass to the satellite
        central_angle (float, rad): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        elevation_angle (float, rad): the distance from the ground station to the satellite

    """
    gamma_rad = radians(central_angle)
    elev = acos(
        sin(gamma_rad)
        / sqrt(
            1
            + (planet_radius / orbital_radius) ** 2
            - 2 * (planet_radius / orbital_radius) * cos(gamma_rad)
        )
    )
    return degrees(elev)


def area_of_coverage(central_angle: float, planet_radius: float = EARTH_RADIUS):
    """
    Calculate the surface area coverage of the Earth from a satellite

    Parameters
    ----------
        central_angle (float, deg): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        area_coverage (float, km): the area of the Earth's surface visible from a satellite

    """
    return 2 * pi * (planet_radius**2) * (1 - cos(radians(central_angle)))


def percentage_of_coverage(
    central_angle: float, planet_radius: float = EARTH_RADIUS
) -> float:
    """
    Calculate the surface area coverage of the Earth from a satellite as a percentage of the total
        surface area

    Parameters
    ----------
        central_angle (float, rad): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        area_coverage (float, %): the percentage of the Earth's surface visible from a satellite

    """
    return (
        area_of_coverage(central_angle, planet_radius)
        / (4 * pi * planet_radius**2)
        * 100
    )


def percentage_of_coverage_gamma(central_angle: float) -> float:
    """
    Calculate the surface area coverage of the Earth from a satellite as a percentage of the total
        surface area

    Parameters
    ----------
        central_angle (float, rad): angle from the satellite to the ground station, centred at the centre of mass

    Return
    ------
        area_coverage (float, %): the percentage of the Earth's surface visible from a satellite

    """
    gamma_rad = radians(central_angle)
    return 50 * (1 - cos(gamma_rad))


def azimuth_intermediate(
    ground_station_lat: float, ground_station_long: float, sat_long: float
) -> float:
    """
    Calculate the azimuth of a geostationary satellite

    Parameters
    ---------
        ground_station_lat (float, deg): the latitude of the ground station
        ground_station_long (float, deg): the longitude of the ground station
        sat_long (float, deg): the longitude of the satellite

    Returns
    ------
        azimuth (float, rad): horizontal pointing angle of the ground station antenna to
            the satellite. The azimuth angle is usually measured in clockwise direction
            in degrees from true north.
    """
    gs_lat_rad = radians(ground_station_lat)
    gs_long_rad = radians(ground_station_long)
    sat_long_rad = radians(sat_long)
    az = atan(tan(abs(sat_long_rad - gs_long_rad)) / sin(gs_lat_rad))
    return degrees(az)


def max_visible_distance(
    orbital_radius: float,
    ground_station_lat: float,
    min_angle: float = 0.0,
    planet_radius: float = EARTH_RADIUS,
) -> float:
    """
    Calculate the radius of visibility for a satellite and a ground station

    Parameters
    ---------
        orbital_radius (float, km): the radius of the satellite from the centre of the Earth
        ground_station_lat (float, deg): the latitude of the ground station
        min_angle (float, deg): the minimum angle of visibility over the horizon
        planet_radius (float, km, optional): radius of the planet

    Returns
    ------

    """
    gs_lat_rad = radians(ground_station_lat)
    min_angle_rad = radians(min_angle)
    return acos(
        cos(
            (
                acos((planet_radius / orbital_radius) * cos(min_angle_rad))
                - min_angle_rad
            )
            / cos(gs_lat_rad)
        )
    )


def azimuth(
    ground_station_lat: float,
    ground_station_long: float,
    sat_lat: float,
    sat_long: float,
) -> float:
    """
    Calculate the azimuth of a satellite

    Parameters
    ---------
        ground_station_lat (float, deg): the latitude of the ground station
        ground_station_long (float, deg): the longitude of the ground station
        sat_lat (float, deg): the latitude of the satellite
        sat_long (float, deg): the longitude of the satellite

    Returns
    ------
        azimuth (float, rad): horizontal pointing angle of the ground station antenna to
            the satellite. The azimuth angle is usually measured in clockwise direction
            in degrees from true north.
    """
    # Ground station is in northern hemisphere
    # rel_pos = ground_station_long - sat_long
    #
    # if 90 > gs_long_rad > 0:
    #
    # At the equator
    # In the southern hemisphere
    # elif 0 > gs_long_rad >= -`90:
    #    if (sat_lat - ground_station_lat)
    #        return pi / 2
    #    else:
    # raise ValueError("Invalid value for the ground station's longitude: must be in range -90 < L < 90")
