import numpy as np

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
