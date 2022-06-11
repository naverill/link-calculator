import numpy as np

from link_calculator.constants import SPEED_OF_LIGHT


def decibel_to_watt(decibels: float):
    """
    Convert decibel watt units to watts

    Parameters
    ----------
      decibels (float, dBW): decibel value

    Returns
    -------
      watts (float, W): Watt value
    """
    return 10 ** (decibels / 10)


def watt_to_decibel(watts: float):
    """
    Convert watts to decibel watts

    Parameters
    ----------
      watts (float, W): Watt value

    Returns
    -------
      decibels (float, dBW): decibel value
    """
    return 10 * np.log10(watts)


def frequency_to_wavelength(frequency: float) -> float:
    """
    Convert frequency to wavelength

    Parameters
    ----------
      frequency (float, GHz): the frequency of the wave

    Returns
    -------
      wavelength (float, m): length of the wave between peaks
    """
    return SPEED_OF_LIGHT / (frequency * 1e9)


def wavelength_to_frequency(wavelength: float) -> float:
    """
    Convert frequency to wavelength

    Parameters
    ----------
      wavelength (float, m): length of the wave between peaks

    Returns
    -------
      frequency (float, GHz): the frequency of the wave
    """
    return (SPEED_OF_LIGHT / wavelength) * 1e-9
