import numpy as np

from link_calculator.constants import SPEED_OF_LIGHT


def decibel_to_watt(value: float):
    """
    Convert decibel watt units to watts

    Parameters
    ----------
      decibels (float, dBW): decibel value

    Returns
    -------
      watts (float, W): Watt value
    """
    if value is None:
        return None
    return 10 ** (value / 10)


def watt_to_decibel(value: float):
    """
    Convert watts to decibel watts

    Parameters
    ----------
      watts (float, W): Watt value

    Returns
    -------
      decibels (float, dBW): decibel value
    """
    if value is None:
        return None
    return 10 * np.log10(value)


def frequency_to_wavelength(value: float) -> float:
    """
    Convert frequency to wavelength

    Parameters
    ----------
      frequency (float, GHz): the frequency of the wave

    Returns
    -------
      wavelength (float, m): length of the wave between peaks
    """
    if value is None:
        return None
    return SPEED_OF_LIGHT / (value * 1e9)


def wavelength_to_frequency(value: float) -> float:
    """
    Convert frequency to wavelength

    Parameters
    ----------
      wavelength (float, m): length of the wave between peaks

    Returns
    -------
      frequency (float, GHz): the frequency of the wave
    """
    if value is None:
        return None
    return (SPEED_OF_LIGHT / value) * 1e-9
