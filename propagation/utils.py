from math import atan2, cos, radians

import numpy as np


def calc_power_density(power: float, distance: float) -> float:
    """
    Calculate the power density of the wavefront

    Parameters
    ---------
        power (float, W): the transmitted power
        distance (float, m): the distance between the transmit and receive antennas

    Returns
    ------
        power_density (float, W/m^2): the power density at distance d
    """
    return power / (4 * np.pi * distance ** 2)


def calc_eirp(power: float, loss: float, gain: float) -> float:
    """
    Calculate the Effetive Isotropic Radiated Power

    Parameters
    ----------
        power (float, W): the total output amplifier power
        loss (float, ): coupling loss between transmitter and antenna
            in the range [0, 1]
        gain (float, ): transmitter gain in the direction of the
            receiving antenna

    Returns
    -------
        eirp (float, dB): power incident at the receiver that would have had to be radiated
            from an isotropic antenna to achieve the same power incident at the
            receiver  as that of a transmitter with a specific antenna gain
    """
    return power * loss * gain


def calc_power_density_eirp(
    eirp: float, distance: float, atmospheric_loss: float
) -> float:
    """
    Calculate the power density of the wavefront using EIRP

    Parameters
    ---------
        eirp (float, dB)
        distance (float, m): the distance between the transmit and receive antennas
        atmospheric_loss (float, ): the total losses due to the atmosphere

    Returns
    ------
        power_density (float, W/m^2): the power density at distance d
    """
    return eirp / (4 * np.pi * distance ** 2)


def calc_effective_aperture(gain: float, wavelength: float) -> float:
    """
    Calculate the effective area of the receiving antenna

    Parameters
    ----------
        gain (float, ): gain of the receive antenna
        wavelength (float, m): the radiation wavelength

    Returns
    -------
        effective_aperture (float, m^2): the effive aperture of the receive antenna
    """
    return gain * wavelength ** 2 / (4 * np.pi)


def calc_receive_power(
    amp_power: float,
    transmit_loss: float,
    transmit_gain: float,
    distance: float,
    receive_gain: float,
    receive_loss: float,
    wavelength: float,
    atmospheric_loss,
) -> float:
    """
    Calculate the power collected by the receive antenna

    Parameters
    ----------
        amp_power (float, W): the total output amplifier power
        power_density (float, W/m^2): the power density at distance d
        transmit_loss (float, ): coupling loss between transmitter and antenna
            in the range [0, 1]
        transmit_gain (float, ): transmitter gain in the direction of the
            receiving antenna
        distance (float, m): the distance between the transmit and receive antennas
        receive_gain (float, ): the gain at the recieve antenna
        receive_loss (float, ): coupling loss between receiver terminals and antenna
            in the range [0, 1]
        wavelength (float, m): the radiation wavelength
        atmospheric_loss (float, ): The loss due to the atmosphere

    Returns
    -------
        receive_power (float, W): the total collected power at the receiver's terminals
    """
    eirp = calc_eirp(amp_power, transmit_loss, transmit_gain)
    pow_density = calc_power_density_eirp(eirp, distance, atmospheric_loss)
    eff_aperture = calc_effective_aperture(receive_gain, wavelength)

    return pow_density * eff_aperture * receive_loss


def calc_free_space_loss(distance: float, wavelength: float) -> float:
    return (wavelength / (4 * np.pi * distance)) ** 2


def calc_free_space_loss_db(distance: float, frequency: float):
    """
    Calculate the free space loss between two antennas

    Parameters
    ----------
        distance (float, m): slant range between the transmit and receive antennas
        frequency (float, GHz): frequency of the transmitter

    Returns
    -------
        path_loss (float, dB): The path loss over the
    """
    return -92.44 - 20 * np.log(distance) * frequency


def calc_slant_path(
    elevation_angle: float,
    rain_altitude: float,
    station_altitude: float,
    refraction_radius: float = 8500,
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


def calc_specific_attenuation(frequency: float, rain_rate: float = 0.01) -> float:
    def func(aj: list, bj, list, cj: list, mk: float, ck: float):
        return sum(
            [
                aj[i] * np.exp(-(((np.log10(frequency) - bj[i]) / cj[i]) ** 2))
                + mk * np.log10(frequency)
                + ck
                for i in range(len(aj))
            ]
        )

    k_const = {
        "mk": -0.18961,
        "ck": 0.71147,
        "aj": [-5.33980, -0.35351, -0.23789, -0.94158],
        "bj": [-0.10008, 1.26970, 0.86036, 0.64552],
        "cj": [1.13098, 0.45400, 0.15354, 0.16817],
    }
    alpha_const = {
        "mk": 0.67849,
        "ck": -1.95537,
        "aj": [-0.14318, 0.29591, 0.32177, -5.3761, 16.172],
        "bj": [1.82442, 0.77564, 0.63773, -0.9623, -3.2998],
        "cj": [-0.55187, 0.19822, 0.13164, 1.47828, 3.43990],
    }
    k = 10 ** (
        func(k_const["aj"], k_const["bj"], k_const["cj"], k_const["mk"], k_const["ck"])
    )
    alpha = func(
        alpha_const["aj"],
        alpha_const["bj"],
        alpha_const["cj"],
        alpha_const["mk"],
        alpha_const["ck"],
    )
    return k * rain_rate ** alpha


def calc_rain_attenuation(
    elevation_angle: float,
    slant_path: float,
    frequency: float,
    rain_altitude: float,
    station_altitude: float,
    station_latitude: float,
    rain_rate: float = 0.01,
) -> float:
    elevation_angle_rad = radians(elevation_angle)
    horiz_proj = slant_path * np.cos(elevation_angle_rad)

    specific_attenuation = calc_specific_attenuation(rain_rate, frequency)
    horiz_reduction = 1 / (
        1
        + 0.78 * np.sqrt(horiz_proj * specific_attenuation / frequency)
        - 0.38 * (1 - np.e ** (-2 * horiz_proj))
    )

    zeta = atan2(horiz_proj * horiz_reduction, rain_altitude - station_altitude)

    if zeta > elevation_angle:
        d_r = horiz_proj * horiz_reduction / np.cos(elevation_angle_rad)
    else:
        d_r = slant_path

    if abs(station_latitude) < 36:
        chi = 36 - abs(station_latitude)
    else:
        chi = 0

    vert_reduction = 1 / (
        1
        + np.sqrt(
            np.sin(elevation_angle_rad)
            * (
                31
                * (1 - np.e ** (-elevation_angle / (1 + chi)))
                * (np.sqrt(d_r * specific_attenuation) / frequency ** 2)
                - 0.45
            )
        )
    )
    effective_path = slant_path * vert_reduction

    return specific_attenuation * effective_path


def calc_worst_rain_rate(rain_rate: float) -> float:
    return (rain_rate / 0.3) ** 0.87


def calc_polarization_loss(faraday_rotation: float) -> float:
    rotation_rad = radians(faraday_rotation)
    return 20 * np.log(cos(rotation_rad))
