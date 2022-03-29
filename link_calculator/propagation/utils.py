from math import atan2, cos, radians, degrees

import numpy as np


def power_density(power: float, distance: float) -> float:
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


def eirp(power: float, loss: float, gain: float) -> float:
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


def power_density_eirp(
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


def effective_aperture(gain: float, wavelength: float) -> float:
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


def receive_power(
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
    eirp = eirp(amp_power, transmit_loss, transmit_gain)
    pow_density = power_density_eirp(eirp, distance, atmospheric_loss)
    eff_aperture = effective_aperture(receive_gain, wavelength)

    return pow_density * eff_aperture * receive_loss


def free_space_loss(distance: float, wavelength: float) -> float:
    """
    Calculate the free space loss between two antennas

    Parameters
    ----------
        distance (float, km): distance between the transmit and receive antennas
        frequency (float, GHz): frequency of the transmitter

    Returns
    -------
        path_loss (float, )
        
    """
    return (wavelength / (4 * np.pi * distance)) ** 2


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


k_h_const = {
    "mk": -0.18961,
    "ck": 0.71147,
    "a": [-5.33980, -0.35351, -0.23789, -0.94158],
    "b": [-0.10008, 1.26970, 0.86036, 0.64552],
    "c": [1.13098, 0.45400, 0.15354, 0.16817],
}
alpha_h_const = {
    "mk": 0.67849,
    "ck": -1.95537,
    "a": [-0.14318, 0.29591, 0.32177, -5.3761, 16.172],
    "b": [1.82442, 0.77564, 0.63773, -0.9623, -3.2998],
    "c": [-0.55187, 0.19822, 0.13164, 1.47828, 3.43990],
}
# Vertical 
k_v_const = {
    "mk": -0.16398, 
    "ck": 0.63297,
    "a": [-3.80595, -3.44965, -0.39902, 0.50167],
    "b": [0.56934, -0.22911, 0.73042, 1.07319],
    "c": [0.81061, 0.51059, 0.11899, 0.27195]
}
alpha_v_const = {
    "mk": -0.053739,
    "ck": 0.83433,
    "a": [-0.07771, 0.56727, -0.20238, -48.2991, 48.5833],
    "b": [2.33840, 0.95545, 1.14520, 0.791669, 0.791459],
    "c": [-0.76284, 0.54039, 0.26809, 0.116226, 0.116479]
}
def specific_attenuation(frequency: float, rain_rate: float = 0.01, polarization: str = "vertical") -> float:
    def calc(consts) -> float: 
        return sum(
            [
                consts["a"][i] * np.exp(-(((np.log10(frequency) - consts["b"][i]) / consts["c"][i]) ** 2))
                for i in range(len(consts["a"]))
            ] 
        ) + consts["mk"] * np.log10(frequency) + consts["ck"]

    if polarization == "vertical": 
        k = 10 ** (
            calc(k_v_const)
        )
        alpha = calc(alpha_v_const)
    elif polarization == "horizontal":
        k = 10 ** (
            calc(k_h_const)
        )
        alpha = calc(alpha_h_const)
    elif polarization == "circular":
        k_v = 10 ** (
            calc(k_v_const)
        )
        alpha_v = calc(alpha_v_const)
        
        k_h = 10 ** (
            calc(k_h_const)
        )
        alpha_h = calc(alpha_h_const)

        k = (k_h + k_v) / 2
        alpha = (k_h * alpha_h + k_v * alpha_v) / (2 * k)
    else:
        raise Exception("Invalid Polarization")

    return k, alpha, k * rain_rate ** alpha


def horizontal_reduction(horizontal_projection: float, specific_attenuation: float, frequency: float) -> float:
    return 1 / (
        1
        + 0.78 * np.sqrt(horizontal_projection * specific_attenuation / frequency)
        - 0.38 * (1 - np.exp(-2 * horizontal_projection))
    )


def vertical_reduction(elevation_angle: float, specific_attenuation: float, d_r: float, frequency: float, chi: float) -> float:
    return 1 / (
        1
        + np.sqrt(np.sin(radians(elevation_angle))) * (
                31
                * (1 - np.exp(-elevation_angle / (1 + chi)))
                * (np.sqrt(d_r * specific_attenuation) / frequency ** 2)
                - 0.45
            )
    )


def zeta(rain_altitude: float, station_altitude: float, horizontal_projection: float, horizontal_reduction: float) -> float:
    return degrees(atan2(rain_altitude - station_altitude, horizontal_projection * horizontal_reduction))


def rain_attenuation(
    elevation_angle: float,
    slant_path: float,
    frequency: float,
    rain_altitude: float,
    station_altitude: float,
    station_latitude: float,
    rain_rate: float = 0.01,
    polarization: str = "vertical"
) -> float:
    elevation_angle_rad = radians(elevation_angle)
    horiz_proj = slant_path * np.cos(elevation_angle_rad)

    _, _, specific_att = specific_attenuation(rain_rate, frequency, polarization)

    horiz_reduction = horizontal_reduction(horiz_proj, specific_att, frequency)

    zeta_ = zeta(rain_altitude, station_altitude, horizontal_projection, horizontal_reduction) 

    if zeta_ > elevation_angle:
        d_r = horiz_proj * horiz_reduction / np.cos(elevation_angle_rad)
    else:
        d_r = slant_path
    
    if abs(station_latitude) < 36:
        chi = 36 - abs(station_latitude)
    else:
        chi = 0

    vert_reduction = vertical_reduction(elevation_angle, specific_att, d_r, frequency, chi) 
    effective_path = slant_path * vert_reduction

    return specific_att * effective_path


def worst_rain_rate(rain_rate: float) -> float:
    return (rain_rate / 0.3) ** 0.87


def polarization_loss(faraday_rotation: float) -> float:
    rotation_rad = radians(faraday_rotation)
    return 20 * np.log(cos(rotation_rad))
