from math import log2, pi, sin, sqrt

from scipy.special import erfc


class PhaseShiftKeying:
    def __init__(
        self,
        bandwidth: float,
        energy_per_symbol: float,
        symbol_rate: float,
        symbol_period: float,
        bits_per_symbol: float,
    ):
        self._bandwidth = bandwidth
        self._energy_per_symbol = energy_per_symbol
        self._symbol_rate = symbol_rate
        self._symbol_period = symbol_period
        self._bits_per_symbol = bits_per_symbol

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_noise is None:
            self._carrier_noise = self.carrier_power / (
                self.noise_power * self.bandwidth
            )
        return self._carrier_noise

    @property
    def eb_no(self) -> float:
        return

    @property
    def carrier_power(self) -> float:
        if self._carrier_power is None:
            self._carrier_power = self.energy_per_symbol * self.symbol_rate
        return self._carrier_power

    @property
    def symbol_rate(self) -> float:
        if self._symbol_rate is None:
            self._symbol_rate = 1.0 / self.symbol_period
        return self._symbol_rate

    @property
    def symbol_period(self) -> float:
        if self._symbol_period is None:
            self._symbol_period = 1.0 / self.symbol_rate
        return self._symbol_period

    @property
    def spectral_efficiency(self) -> float:
        if self._spectral_efficiency is None:
            self._spectral_efficiency = (
                self.bit_rate * log2(self.M) / (self.bandwidth * self.symbol_period)
            )


class BinaryPhaseShiftKeying(PhaseShiftKeying):
    M = 2

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            self._noise_probability = 0.5 * erfc(sqrt(self.carrier_to_noise))
        return self._noise_probability

    @property
    def bit_error_rate(self) -> float:
        if self._bit_error_rate is None:
            self._bit_error_rate = self.noise_probability / self.bits_per_symbol
        return self._bit_error_rate


class QuadraturePhaseShiftKeying(PhaseShiftKeying):
    M = 4

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            self._noise_probability = 0.5 * erfc(sqrt(self.carrier_to_noise * 0.5))
        return self._noise_probability

    @property
    def bit_error_rate(self) -> float:
        if self._bit_error_rate is None:
            self._bit_error_rate = self.noise_probability / self.bits_per_symbol
        return self._bit_error_rate


class MPhaseShiftKeying(PhaseShiftKeying):
    def __init__(self, n_phases: float):
        self.M = n_phases

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            self._noise_probability = erfc(
                sqrt(self.bits_per_symbol * self.energy_per_bit / self.noise_power)
                * sin(pi / self.M)
            )
        return self._noise_probability

    @property
    def bit_error_rate(self) -> float:
        if self._bit_error_rate is None:
            self._bit_error_rate = self.noise_probability / self.bits_per_symbol
        return self._bit_error_rate
