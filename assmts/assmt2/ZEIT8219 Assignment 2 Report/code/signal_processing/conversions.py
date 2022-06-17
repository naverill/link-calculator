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
