from math import acos, atan, atan2, cos, degrees, pi, radians, sin, sqrt, tan

from link_calculator.constants import EARTH_MU, EARTH_RADIUS


def velocity(
    semi_major_axis: float, orbital_radius: float, mu: float = EARTH_MU
) -> float:
    """
    Calculate the velocity of a satellite in orbit according to Kepler's second law

    Parameters
    ---------
        semi_major_axis (float, km): The semi-major axis of the orbit
            orbital_radius (float, km): distance from the centre of mass to the satellite
        mu (float, optional): Kepler's gravitational constant

    Returns
    ------
        velocity (float, km/s): the orbit speed of the satellite
    """
    return sqrt(mu * (2 / orbital_radius - 1 / semi_major_axis))


def velocity_circular(orbital_radius: float, mu: float = EARTH_MU) -> float:
    """
    Special case of velocity where r = a

    Parameters
    ---------
        orbital_radius (float, km): distance from the centre of mass to the satellite
        mu (float, optional): Kepler's gravitational constant

    Returns
    ------
        velocity (float, km/s): the orbit speed of the satellite
    """
    return velocity(orbital_radius, orbital_radius, mu)


def period(semi_major_axis: float, mu: float = EARTH_MU) -> float:
    """
    Calculate the period of the satellite's orbit according to Kepler's third law

    Parameters
    ---------
        semi_major_axis (float, km): The semi-major axis of the orbit
        mu (float, km^3/s^-2, optional): Kepler's gravitational constant

    Returns
    ------
        period (float, s): the time taken for the satellite to complete a revolution
    """
    return 2 * pi * sqrt(semi_major_axis**3 / mu)


def angle_sat_to_ground_station(
    ground_station_lat: float,
    ground_station_long: float,
    sat_lat: float,
    sat_long: float,
) -> float:
    """
    Calculate angle gamma at the centre of the ground, between the Earth station and the satellite

    Parameters
    ---------
        ground_station_lat (float, deg): the latitude of the ground station
        ground_station_long (float, deg): the longitude of the ground station
        sat_lat (float, deg): the latitude of the satellite
        sat_long (float, deg): the longitude of the satellite

    Returns
    ------
        gamma (float, rad): angle between satellite and ground station
    """
    gs_lat_rad = radians(ground_station_lat)
    gs_long_rad = radians(ground_station_long)
    sat_lat_rad = radians(sat_lat)
    sat_long_rad = radians(sat_long)

    gamma = acos(
        cos(gs_lat_rad) * cos(sat_lat_rad) * cos(sat_long_rad - gs_long_rad)
        + sin(gs_lat_rad) * sin(sat_lat_rad)
    )
    return degrees(gamma)


def angle_sat_to_gs_orbital_radius(
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
    orbital_radius: float, angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS
) -> float:
    """
    Calculate the slant range from the ground station to the satellite

    Parameters
    ----------
        orbital_radius (float, km): distance from the centre of mass to the satellite
        angle_sat_to_gs (float, deg): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        slant_range (float, km): the distance from the ground station to the satellite

    """
    return sqrt(
        planet_radius**2
        + orbital_radius**2
        - 2 * planet_radius * orbital_radius * cos(radians(angle_sat_to_gs))
    )


def elevation_angle(
    orbital_radius: float, angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS
) -> float:
    """
    Calculate the elevation angle from the ground station to the satellite

    Parameters
    ----------
        orbital_radius (float, km): distance from the centre of mass to the satellite
        angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        elevation_angle (float, rad): the distance from the ground station to the satellite

    """
    gamma_rad = radians(angle_sat_to_gs)
    elev = acos(
        sin(gamma_rad)
        / sqrt(
            1
            + (planet_radius / orbital_radius) ** 2
            - 2 * (planet_radius / orbital_radius) * cos(gamma_rad)
        )
    )
    return degrees(elev)


def area_of_coverage(angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS):
    """
    Calculate the surface area coverage of the Earth from a satellite

    Parameters
    ----------
        angle_sat_to_gs (float, deg): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        area_coverage (float, km): the area of the Earth's surface visible from a satellite

    """
    angle_sat_to_gs_rad = radians(angle_sat_to_gs)
    return 2 * pi * (planet_radius**2) * (1 - cos(angle_sat_to_gs_rad))


def percentage_of_coverage(
    angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS
) -> float:
    """
    Calculate the surface area coverage of the Earth from a satellite as a percentage of the total
        surface area

    Parameters
    ----------
        angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass
        planet_radius (float, km, optional): radius of the planet

    Return
    ------
        area_coverage (float, %): the percentage of the Earth's surface visible from a satellite

    """
    return (
        area_of_coverage(angle_sat_to_gs, planet_radius)
        / (4 * pi * planet_radius**2)
        * 100
    )


def percentage_of_coverage_gamma(angle_sat_to_gs: float) -> float:
    """
    Calculate the surface area coverage of the Earth from a satellite as a percentage of the total
        surface area

    Parameters
    ----------
        angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass

    Return
    ------
        area_coverage (float, %): the percentage of the Earth's surface visible from a satellite

    """
    gamma_rad = radians(angle_sat_to_gs)
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
    ## At the equator
    ## In the southern hemisphere
    # elif 0 > gs_long_rad >= -`90:
    #    if (sat_lat - ground_station_lat)
    #        return pi / 2
    #    else:
    # raise ValueError("Invalid value for the ground station's longitude: must be in range -90 < L < 90")
