import numpy as np


def axes_to_eccentricity(a: float, b: float):
    return np.sqrt(a**2, b**2) / a
