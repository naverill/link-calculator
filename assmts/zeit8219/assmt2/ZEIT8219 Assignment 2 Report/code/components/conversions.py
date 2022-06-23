from math import log10


def joules_to_decibel_joules(value: float) -> float:
    if value is None:
        return None
    return 10 * log10(value)


def decibel_joules_to_joules(value: float) -> float:
    if value is None:
        return None
    return 10 ** (value / 10)
