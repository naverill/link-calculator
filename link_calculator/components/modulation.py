from math import log2, pi, sin, sqrt

from scipy.special import erfc


class PhaseShiftKeying:
    def __init__(
        self,
        levels: float,
        bandwidth: float = None,
        energy_per_symbol: float = None,
        symbol_rate: float = None,
        symbol_period: float = None,
        bit_rate: float = None,
        bit_period: float = None,
        bits_per_symbol: float = None,
        carrier_power: float = None,
    ):
        self._levels = levels
        self._bandwidth = bandwidth
        self._energy_per_symbol = energy_per_symbol
        self._symbol_rate = symbol_rate
        self._symbol_period = symbol_period
        self._bits_per_symbol = bits_per_symbol
        self._bit_rate = bit_period
        self._bit_period = bit_period
        self._carrier_power = carrier_power

    @property
    def frequency_deviation(self) -> float:
        if self._frequency_deviation is None:
            self._frequency_deviation = None

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_noise is None:
            self._carrier_noise = self.carrier_power / (
                self.noise_power * self.bandwidth
            )
        return self._carrier_noise

    @property
    def eb_no(self) -> float:
        if self._eb_no is None:
            self._eb_no = (
                self.carrier_power
                * self.bandwidth
                / (self.noise_power * self.symbol_rate)
            )
        return self._eb_no

    @property
    def carrier_power(self) -> float:
        if self._carrier_power is None:
            self._carrier_power = self.energy_per_symbol * self.symbol_rate
        return self._carrier_power

    @property
    def bits_per_symbol(self):
        if self._bits is None:
            self.bits = log2(self.levels)
        return self._bits

    @property
    def bit_rate(self) -> float:
        if self._bit_rate is None:
            self._bit_rate = 1.0 / self.bit_period
        return self._bit_rate

    @property
    def bit_period(self) -> float:
        if self._bit_period is None:
            self._bit_period = self.symbol_period / self.bits_per_symbol
        return self._bit_period

    @property
    def symbol_rate(self) -> float:
        if self._symbol_rate is None:
            self._symbol_rate = self.bit_rate / self.bits_per_symbol
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
                self.bit_rate
                * log2(self.levels)
                / (self.bandwidth * self.symbol_period)
            )

    @property
    def energy_per_symbol(self) -> float:
        if self._energy_per_symbol is None:
            self._energy_per_symbol = self.carrier_power * self.symbol_period
        return self._energy_per_symbol

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            self._noise_probability = erfc(
                sqrt(self.bits_per_symbol * self.energy_per_bit / self.noise_power)
                * sin(pi / self.levels)
            )
        return self._noise_probability

    @property
    def bit_error_rate(self) -> float:
        if self._bit_error_rate is None:
            self._bit_error_rate = self.noise_probability / self.bits_per_symbol
        return self._bit_error_rate


class BinaryPhaseShiftKeying(PhaseShiftKeying):
    def __init__(
        self,
        bandwidth: float = None,
        energy_per_symbol: float = None,
        symbol_rate: float = None,
        symbol_period: float = None,
        bit_rate: float = None,
        bit_period: float = None,
        bits_per_symbol: float = None,
    ):
        super().__init__(
            levels=2,
            bandwidth=bandwidth,
            energy_per_dymbol=energy_per_symbol,
            symbol_rate=symbol_rate,
            bit_rate=bit_rate,
            bit_period=bit_period,
            bits_per_symbol=bits_per_symbol,
        )

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
    def __init__(
        self,
        bandwidth: float = None,
        energy_per_symbol: float = None,
        symbol_rate: float = None,
        symbol_period: float = None,
        bit_rate: float = None,
        bit_period: float = None,
        bits_per_symbol: float = None,
    ):
        super().__init__(
            levels=4,
            bandwidth=bandwidth,
            energy_per_dymbol=energy_per_symbol,
            symbol_rate=symbol_rate,
            bit_rate=bit_rate,
            bit_period=bit_period,
            bits_per_symbol=bits_per_symbol,
        )

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
