from math import erfc, log2, log10, pi, sin, sqrt

import pandas as pd
from scipy.special import erfcinv

from link_calculator.conversions import (
    GHz_to_Hz,
    Hz_to_GHz,
    Hz_to_MHz,
    bit_to_mbit,
    mbit_to_bit,
    watt_to_decibel,
)
from link_calculator.signal_processing.coding import ConvolutionalCode


class Waveform:
    def __init__(
        self, frequency: float = None, amplitude: float = None, phase: float = None
    ):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase


class Modulation:
    def __init__(
        self,
        bandwidth: float = None,
        carrier_to_noise: float = None,
    ):
        self._bandwidth = bandwidth
        self._carrier_to_noise = carrier_to_noise

    @property
    def channel_capacity(self) -> float:
        return self.bandwidth * log2(1 + self.carrier_to_noise)

    @property
    def channel_capacity_to_bandwidth_ideal(self) -> float:
        return log2(1 + self.eb_no * self.channel_capacity / self.bandwidth)

    @property
    def channel_capacity_to_bandwidth(self) -> float:
        return log2(1 + self.eb_no * self.bit_rate / self.bandwidth)

    @property
    def eb_no(self) -> float:
        return (2 ** (self.channel_capacity / self.bandwidth) - 1) / (
            self.channel_capacity / self.bandwidth
        )


class MPhaseShiftKeying(Modulation):
    def __init__(
        self,
        levels: int,
        bandwidth: float = None,
        carrier_signal: Waveform = None,
        modulating_signal: Waveform = None,
        energy_per_symbol: float = None,
        energy_per_bit: float = None,
        symbol_rate: float = None,
        symbol_period: float = None,
        bit_rate: float = None,
        bit_error_rate: float = None,
        bit_error_rate_coded: float = None,
        bit_period: float = None,
        bits_per_symbol: int = None,
        carrier_power: float = None,
        coding_rate: float = None,
        carrier_to_noise: float = None,
        carrier_to_noise_coded: float = None,
        spectral_efficiency: float = None,
        eb_no: float = None,
        eb_no_coded: float = None,
        es_no: float = None,
        es_no_coded: float = None,
        rolloff_rate: float = None,
        frequency_range: list = None,
        noise_probability: float = None,
        noise_probability_coded: float = None,
        noise_power_density: float = None,
        noise_power_density_coded: float = None,
        code: ConvolutionalCode = None,
        data_rate: float = None,
    ):
        """
        Parameters
        ----------
            levels (int,): number of levels in the waveform (equivalent to number of symbols)
            bandwidth (float, GHz): the range of frequencies required to transmit the signal
            energy_per_symbol (float, J): energy required to transmit one symbol
            energy_per_bit (float, J): energy required to transmit one bit
            symbol_rate (float, symbols/s): number of symbols transmitted per second
            symbol_period (float, s/symbol): seconds to transmit a symbol
            bit_rate (float, bits/s): number of bits transmitted per second
            bit_period (float, s/bit): number of seconds to transmit a bit
            carrier_power (float, W): total transmit power of signal
            spectral_efficiency (float bit/s/Hz):
        """
        self._levels = levels
        self._bandwidth = bandwidth
        self._energy_per_symbol = energy_per_symbol
        self._energy_per_bit = energy_per_bit
        self._symbol_rate = symbol_rate
        self._symbol_period = symbol_period
        self._bits_per_symbol = bits_per_symbol
        self._bit_rate = bit_rate
        self._bit_error_rate = bit_error_rate
        self._bit_period = bit_period
        self._carrier_power = carrier_power
        self._carrier_to_noise = carrier_to_noise
        self._eb_no = eb_no
        self._es_no = es_no
        self._rolloff_rate = rolloff_rate
        self._carrier_signal = carrier_signal
        self._modulating_signal = modulating_signal
        self._frequency_range = frequency_range
        self._spectral_efficiency = spectral_efficiency
        self._noise_probability = noise_probability
        self._code = code
        self._data_rate = data_rate
        self._bit_error_rate_coded = bit_error_rate_coded
        self._carrier_to_noise_coded = carrier_to_noise_coded
        self._eb_no_coded = eb_no_coded
        self._noise_power_density_coded = noise_power_density_coded
        self._noise_power_density = noise_power_density
        self._noise_probability_coded = noise_probability_coded
        self._es_no_coded = es_no_coded
        self.propagate_calculations()

    @property
    def es_no(self) -> float:
        if self._es_no is None:
            if self._isset(self._carrier_to_noise):
                self._es_no = (
                    self.carrier_to_noise * GHz_to_Hz(self.bandwidth) / self.symbol_rate
                )
            elif self._isset(self._eb_no):
                return self.eb_no * self.bits_per_symbol
        return self._es_no

    @property
    def es_no_coded(self) -> float:
        if self._es_no_coded is None:
            if self._isset(
                self._carrier_to_noise_coded, self._bandwidth, self._symbol_rate
            ):
                self._es_no = (
                    self.carrier_to_noise_coded
                    * GHz_to_Hz(self.bandwidth)
                    / self.symbol_rate
                )
            elif self._isset(self._eb_no_coded):
                return self.eb_no_coded * self.bits_per_symbol
        return self._es_no_coded

    @property
    def eb_no(self) -> float:
        if self._eb_no is None:
            if self._isset(self._bit_error_rate):
                self._eb_no = (
                    erfcinv(self.bit_error_rate * self.bits_per_symbol)
                    / sin(pi / self.levels)
                ) ** 2 / self.bits_per_symbol
            elif self._isset(self._es_no):
                self._eb_no = self.es_no / self.bits_per_symbol
            elif self._isset(self._energy_per_bit, self._noise_power_density):
                self._eb_no = self.energy_per_bit / self.noise_power_density
        return self._eb_no

    @property
    def eb_no_coded(self) -> float:
        if self._eb_no_coded is None:
            if self._isset(self._code):
                self._eb_no_coded = self.eb_no * self.code.coding_gain
            else:
                self._eb_no_coded = self.eb_no
        return self._eb_no_coded

    @eb_no.setter
    def eb_no(self, value) -> None:
        self._eb_no = value

    @property
    def carrier_power(self) -> float:
        return self._carrier_power

    @carrier_power.setter
    def carrier_power(self, value) -> None:
        self._carrier_power = value

    @property
    def bit_rate(self) -> float:
        if self._bit_rate is None:
            if self._isset(self._bit_period):
                self._bit_rate = 1.0 / self.bit_period
            elif self._isset(self._rolloff_rate):
                self._bit_rate = (
                    self.bits_per_symbol
                    * GHz_to_Hz(self.bandwidth)
                    / (1 + self.rolloff_rate)
                )
        return self._bit_rate

    @property
    def data_rate(self) -> float:
        if self._data_rate is None:
            if self._isset(self._code):
                self._data_rate = self.bit_rate * self.code.coding_rate
            else:
                self._data_rate = self.bit_rate
        return self._data_rate

    @property
    def bit_period(self) -> float:
        if self._bit_period is None:
            self._bit_period = self.symbol_period / self.bits_per_symbol
        return self._bit_period

    @property
    def symbol_rate(self) -> float:
        if self._symbol_rate is None:
            if self._isset(self._bandwidth, self._rolloff_rate):
                self._symbol_rate = (GHz_to_Hz(self._bandwidth)) / (
                    1 + self.rolloff_rate
                )
            else:
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
            if self._isset(self._bit_rate, self._bandwidth):
                self._spectral_efficiency = self.bit_rate / GHz_to_Hz(self.bandwidth)
        return self._spectral_efficiency

    @property
    def energy_per_symbol(self) -> float:
        if self._energy_per_symbol is None:
            if self._isset(self._carrier_power, self._symbol_period):
                self._energy_per_symbol = self.carrier_power * self.symbol_period
        return self._energy_per_symbol

    @property
    def bits_per_symbol(self):
        if self._bits_per_symbol is None:
            self._bits_per_symbol = log2(self.levels)
        return self._bits_per_symbol

    @property
    def energy_per_bit(self) -> float:
        """
        Returns
            energy_per_bit (float, J/s)
        """
        if self._energy_per_bit is None:
            if self._isset(self._carrier_power):
                self._energy_per_bit = self.carrier_power * self.bit_period
        return self._energy_per_bit

    @property
    def noise_power_density(self) -> float:
        if self._noise_power_density is None:
            if self._isset(
                self._symbol_rate, self._carrier_to_noise, self._energy_per_symbol
            ):
                self._noise_power_density = self.symbol_rate / (
                    self.bandwidth * self.carrier_to_noise * self.energy_per_symbol
                )
        return self._noise_power_density

    @property
    def noise_power_density_coded(self) -> float:
        if self._noise_power_density_coded is None:
            if self._isset(
                self._symbol_rate, self._carrier_to_noise_coded, self._energy_per_symbol
            ):
                self._noise_power_density_coded = self.symbol_rate / (
                    self.bandwidth
                    * self.carrier_to_noise_coded
                    * self.energy_per_symbol
                )
        return self._noise_power_density_coded

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            if self._isset(self._es_no):
                self._noise_probability = erfc(sqrt(self.es_no) * sin(pi / self.levels))
        return self._noise_probability

    @property
    def noise_probability_coded(self) -> float:
        if self._noise_probability_coded is None:
            if self._isset(self._eb_no_coded):
                self._noise_probability_coded = erfc(
                    sqrt(self.bits_per_symbol * self.eb_no_coded)
                    * sin(pi / self.levels)
                )
        return self._noise_probability_coded

    @property
    def bit_error_rate(self) -> float:
        if self._bit_error_rate is None:
            if self._isset(self._noise_probability):
                self._bit_error_rate = self.noise_probability / self.bits_per_symbol
        return self._bit_error_rate

    @property
    def bit_error_rate_coded(self) -> float:
        if self._bit_error_rate_coded is None:
            if self._isset(self._noise_probability_coded):
                self._bit_error_rate_coded = (
                    self.noise_probability_coded / self.bits_per_symbol
                )
        return self._bit_error_rate_coded

    @property
    def levels(self) -> float:
        return self._levels

    @property
    def rolloff_rate(self) -> float:
        return self._rolloff_rate

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_to_noise is None:
            if self._isset(self._eb_no):
                self._carrier_to_noise = (
                    self.eb_no * self.bit_rate / GHz_to_Hz(self._bandwidth)
                )
        return self._carrier_to_noise

    @property
    def carrier_to_noise_coded(self) -> float:
        if self._carrier_to_noise_coded is None:
            if self._isset(self._eb_no_coded):
                self._carrier_to_noise_coded = (
                    self.eb_no_coded * self.bit_rate / GHz_to_Hz(self._bandwidth)
                )
        return self._carrier_to_noise_coded

    @property
    def carrier_signal(self) -> Waveform:
        return self._carrier_signal

    @property
    def code(self) -> ConvolutionalCode:
        return self._code

    @property
    def bandwidth(self) -> float:
        if self._bandwidth is None:
            if self._isset(self._symbol_rate, self._rolloff_rate):
                self._bandwidth = self.symbol_rate * (1 + self.rolloff_rate)
        return self._bandwidth

    @property
    def frequency_range(self) -> float:
        if self._frequency_range is None:
            self._frequency_range = [
                self.carrier_signal.frequency - self.bandwidth / 2,
                self.carrier_signal.frequency + self.bandwidth / 2,
            ]
        return self._frequency_range

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Maximum Bit Rate",
                    "unit": "mbps",
                    "value": bit_to_mbit(self.bit_rate),
                },
                {
                    "name": "Data Rate",
                    "unit": "mbps",
                    "value": bit_to_mbit(self.data_rate),
                },
                {"name": "Bandwidth", "unit": "GHz", "value": self.bandwidth},
                {
                    "name": "Spectral Efficiency",
                    "unit": "bits/s/Hz",
                    "value": self.spectral_efficiency,
                },
                {
                    "name": "C/N Ratio",
                    "unit": "bits/s/GHz",
                    "value": watt_to_decibel(self.carrier_to_noise),
                },
                {
                    "name": "Coded C/N Ratio",
                    "unit": "bits/s/GHz",
                    "value": watt_to_decibel(self.carrier_to_noise_coded),
                },
                {
                    "name": "Eb/No Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.eb_no),
                },
                {
                    "name": "Coded Eb/No Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.eb_no_coded),
                },
                {
                    "name": "Bit Error Rate",
                    "unit": "",
                    "value": self.bit_error_rate,
                },
                {
                    "name": "Coded Bit Error Rate",
                    "unit": "",
                    "value": self.bit_error_rate_coded,
                },
                {"name": "Roll-Off Factor", "unit": "", "value": self.rolloff_rate},
            ]
        )
        summary.set_index("name", inplace=True)

        if self._isset(self.code):
            code = self.code.summary()
            summary = pd.concat([summary, code])
        else:
            summary = summary[[not ("Coded" in idx) for idx in summary.index]]

        return summary

    def propagate_calculations(self) -> float:
        for _ in range(4):
            for var in type(self).__dict__:
                getattr(self, var, None)

    def _isset(self, *args) -> bool:
        return not (None in args)


class BinaryPhaseShiftKeying(MPhaseShiftKeying):
    def __init__(
        self,
        bandwidth: float = None,
        carrier_signal: Waveform = None,
        modulating_signal: Waveform = None,
        energy_per_symbol: float = None,
        energy_per_bit: float = None,
        symbol_rate: float = None,
        symbol_period: float = None,
        bit_rate: float = None,
        bit_period: float = None,
        bits_per_symbol: float = None,
        carrier_power: float = None,
        rolloff_rate: float = None,
        frequency_range: list = None,
    ):
        super().__init__(
            levels=2,
            bandwidth=bandwidth,
            carrier_signal=carrier_signal,
            modulating_signal=modulating_signal,
            energy_per_bit=energy_per_bit,
            rolloff_rate=rolloff_rate,
            frequency_range=frequency_range,
            carrier_power=carrier_power,
            energy_per_symbol=energy_per_symbol,
            symbol_rate=symbol_rate,
            bit_rate=bit_rate,
            bit_period=bit_period,
            bits_per_symbol=bits_per_symbol,
        )

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            if self._isset(self._carrier_to_noise):
                self._noise_probability = 0.5 * erfc(sqrt(self.carrier_to_noise))
        return self._noise_probability

    def _isset(self, *args) -> bool:
        return not (None in args)


class QuadraturePhaseShiftKeying(MPhaseShiftKeying):
    def __init__(
        self,
        bandwidth: float = None,
        carrier_signal: Waveform = None,
        modulating_signal: Waveform = None,
        energy_per_symbol: float = None,
        symbol_rate: float = None,
        symbol_period: float = None,
        carrier_power: float = None,
        bit_rate: float = None,
        bit_period: float = None,
        bits_per_symbol: float = None,
        rolloff_rate: float = None,
    ):
        super().__init__(
            levels=4,
            bandwidth=bandwidth,
            carrier_signal=carrier_signal,
            modulating_signal=modulating_signal,
            energy_per_symbol=energy_per_symbol,
            symbol_rate=symbol_rate,
            carrier_power=carrier_power,
            bit_rate=bit_rate,
            bit_period=bit_period,
            bits_per_symbol=bits_per_symbol,
            rolloff_rate=rolloff_rate,
        )

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            if self._carrier_to_noise is not None:
                self._noise_probability = 0.5 * erfc(sqrt(self.carrier_to_noise * 0.5))
        return self._noise_probability
