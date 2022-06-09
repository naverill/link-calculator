from math import atan2, cos, degrees, radians

import numpy as np

from link_calculator.components.antennas import Antenna
from link_calculator.constants import EARTH_RADIUS


def free_space_loss(distance: float, wavelength: float) -> float:
    """
    Calculate the free space loss between two antennas

    Parameters
    ----------
        distance (float, km): distance between the transmit and receive antennas
        wavelength (float, m): frequency of the transmitter

    Returns
    -------
        path_loss (float, )

    """
    return (wavelength / (4 * np.pi * distance * 1000)) ** 2


def free_space_loss_db(slant_range: float, frequency: float):
    """
    Calculate the free space loss between two antennas

    Parameters
    ----------
        slant_range (float, km): slant range between the transmit and receive antennas
        frequency (float, GHz): frequency of the transmitter

    Returns
    -------
        path_loss (float, dB): The path loss over the
    """
    return -92.44 - 20 * np.log10(slant_range * frequency)


def slant_path(
    elevation_angle: float,
    rain_altitude: float,
    station_altitude: float,
) -> float:
    """
    Calculate the slant path

    Parameters
    ----------
        angle_of_elevation (float, deg): the angle between the Earth station and the satellite
        rain_height (float, km): the rain height
        station_altitude (float, km): the rain height of the Earth station above sea level
        refraction_radius (float, km): The modified radius of the Earth to account for the
            refraction of the wave by thr troposphere

    Returns
    -------
        d_s (float, km): The slant height
    """
    refraction_radius = 8500 if station_altitude < 1.0 else EARTH_RADIUS
    elevation_angle_rad = radians(elevation_angle)
    if elevation_angle < 5:
        return (
            2
            * (rain_altitude - station_altitude)
            / np.sqrt(
                np.sin(elevation_angle_rad) ** 2
                + 2 * (rain_altitude - station_altitude) / refraction_radius
            )
        )
    else:
        return (rain_altitude - station_altitude) / np.sin(elevation_angle_rad)


def rain_specific_attenuation(frequency: float, rain_rate: float, polarization: str):
    """
    TODO()

    Parameters
    ----------

    Returns
    -------

    """
    _f = [
        1,
        2,
        4,
        6,
        7,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
        35,
        40,
        45,
        50,
        60,
        70,
        80,
        90,
        100,
        120,
        150,
        200,
        300,
        400,
    ]

    _kH = [
        0.0000387,
        0.000154,
        0.00065,
        0.00175,
        0.00301,
        0.00454,
        0.0101,
        0.0188,
        0.0367,
        0.0751,
        0.124,
        0.187,
        0.263,
        0.35,
        0.442,
        0.536,
        0.707,
        0.851,
        0.975,
        1.06,
        1.12,
        1.18,
        1.31,
        1.45,
        1.36,
        1.32,
    ]

    _kV = [
        0.0000352,
        0.000138,
        0.000591,
        0.00155,
        0.00265,
        0.00395,
        0.00887,
        0.0168,
        0.0335,
        0.0691,
        0.113,
        0.167,
        0.233,
        0.31,
        0.393,
        0.479,
        0.642,
        0.784,
        0.906,
        0.999,
        1.06,
        1.13,
        1.27,
        1.42,
        1.35,
        1.31,
    ]

    _alphaH = [
        0.912,
        0.963,
        1.121,
        1.308,
        1.332,
        1.327,
        1.276,
        1.217,
        1.154,
        1.099,
        1.061,
        1.021,
        0.979,
        0.939,
        0.903,
        0.873,
        0.826,
        0.793,
        0.769,
        0.753,
        0.743,
        0.731,
        0.71,
        0.689,
        0.688,
        0.683,
    ]

    _alphaV = [
        0.88,
        0.923,
        1.075,
        1.265,
        1.312,
        1.31,
        1.264,
        1.2,
        1.128,
        1.065,
        1.03,
        1,
        0.963,
        0.929,
        0.897,
        0.868,
        0.824,
        0.793,
        0.769,
        0.754,
        0.744,
        0.732,
        0.711,
        0.69,
        0.689,
        0.684,
    ]

    KH = np.exp(np.interp(np.log(frequency), np.log(_f), np.log(_kH)))
    KV = np.exp(np.interp(np.log(frequency), np.log(_f), np.log(_kV)))

    alphaH = np.interp(np.log(frequency), np.log(_f), _alphaH)
    alphaV = np.interp(np.log(frequency), np.log(_f), _alphaV)

    if polarization == "circular":
        k = (KH + KV) / 2
        alpha = (KH * alphaH + KV * alphaV) / (2 * k)
    elif polarization == "vertical":
        k = KV
        alpha = alphaV
    elif polarization == "horizontal":
        k = KH
        alpha = alphaH
    else:
        raise Exception("Invalid Polarization")

    return k, alpha, k * rain_rate**alpha


def horizontal_reduction(
    horizontal_projection: float, specific_attenuation: float, frequency: float
) -> float:
    """
    TODO()

    Parameters
    ----------

    Returns
    -------
    """
    return 1 / (
        1
        + 0.78 * np.sqrt(horizontal_projection * specific_attenuation / frequency)
        - 0.38 * (1 - np.exp(-2 * horizontal_projection))
    )


def vertical_adjustment(
    elevation_angle: float,
    specific_attenuation: float,
    d_r: float,
    frequency: float,
    chi: float,
) -> float:
    """
    Calculate the vertical adjustment factor

    Parameters
    ----------
        elevation_angle (float, deg):
        specific_attenation (float, dBKm-1)
        d_r (float, km):
        frequency (float, GHz):
        chi (float, deg):

    Returns
    -------
        vert_adj (float, )
    """
    return 1 / (
        1
        + np.sqrt(np.sin(radians(elevation_angle)))
        * (
            31
            * (1 - np.exp(-elevation_angle / (1 + chi)))
            * (np.sqrt(d_r * specific_attenuation) / (frequency**2))
            - 0.45
        )
    )


def zeta(
    rain_altitude: float,
    station_altitude: float,
    horizontal_projection: float,
    horizontal_reduction: float,
) -> float:
    """
    Calculate interim vertical adjustment value

    Parameters
    ----------

    Returns
    -------
    """
    return degrees(
        atan2(
            rain_altitude - station_altitude,
            horizontal_projection * horizontal_reduction,
        )
    )


def rain_attenuation(
    elevation_angle: float,
    slant_path: float,
    frequency: float,
    rain_altitude: float,
    station_altitude: float,
    station_latitude: float,
    rain_rate: float = 0.01,
    polarization: str = "vertical",
) -> float:
    """

    Parameters
    ----------

    Returns
    -------

    """
    elevation_angle_rad = radians(elevation_angle)
    horiz_proj = slant_path * np.cos(elevation_angle_rad)

    _, _, specific_att = rain_specific_attenuation(frequency, rain_rate, polarization)

    horiz_reduction = horizontal_reduction(horiz_proj, specific_att, frequency)

    zeta_ = zeta(rain_altitude, station_altitude, horiz_proj, horiz_reduction)

    if zeta_ > elevation_angle:
        d_r = horiz_proj * horiz_reduction / np.cos(elevation_angle_rad)
    else:
        d_r = slant_path

    if abs(station_latitude) < 36:
        chi = 36 - abs(station_latitude)
    else:
        chi = 0

    vert_adj = vertical_adjustment(elevation_angle, specific_att, d_r, frequency, chi)
    effective_path = slant_path * vert_adj

    return specific_att * effective_path


def worst_rain_rate(rain_rate: float) -> float:
    return (rain_rate / 0.3) ** 0.87


def polarization_loss(faraday_rotation: float) -> float:
    rotation_rad = radians(faraday_rotation)
    return 20 * np.log(cos(rotation_rad))
