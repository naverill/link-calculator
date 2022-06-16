from math import log10

import numpy as np

from link_calculator.constants import SPEED_OF_LIGHT


def joules_to_decibel_joules(value: float) -> float:
    if value is None:
        return None
    return 10 * log10(value)


def decibel_joules_to_joules(value: float) -> float:
    if value is None:
        return None
    return 10 ** (value / 10)


def MHz_to_GHz(value: float) -> float:
    if value is None:
        return None
    return value * 1e-3


def GHz_to_MHz(value: float) -> float:
    if value is None:
        return None
    return value * 1e3


def GHz_to_Hz(value: float) -> float:
    if value is None:
        return None
    return value * 1e9


def Hz_to_GHz(value: float) -> float:
    if value is None:
        return None
    return value * 1e-9


def MHz_to_Hz(value: float) -> float:
    if value is None:
        return None
    return value * 1e6


def Hz_to_MHz(value: float) -> float:
    if value is None:
        return None
    return value * 1e-6


def mbit_to_bit(value: float) -> float:
    if value is None:
        return None
    return value * 1e6


def bit_to_mbit(value: float) -> float:
    if value is None:
        return None
    return value * 1e-6


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
