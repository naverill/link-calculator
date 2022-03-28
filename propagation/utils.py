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
        power (float, W): amplifier power
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

    Returns
    -------
        receive_power (float, W): the total collected power at the receiver's terminals
    """
    eirp = eirp(amp_power, transmit_loss, transmit_gain)
    pow_density = power_density_eirp(eirp, distance, atmospheric_loss)
    eff_aperture = effective_aperture(receive_gain, wavelength)

    return pow_density * eff_aperture * receive_loss


def free_space_loss(distance: float, wavelength: float) -> float:
    return (wavelength / (4 * np.pi * distance)) ** 2
