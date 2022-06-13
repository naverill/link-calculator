from math import log2, log10, pi, sin, sqrt

import pandas as pd
from scipy.special import erfc, erfcinv

from link_calculator.propagation.conversions import watt_to_decibel
from link_calculator.signal_processing.conversions import (
    GHz_to_Hz,
    Hz_to_GHz,
    Hz_to_MHz,
    bit_to_mbit,
    mbit_to_bit,
)


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


class FrequencyModulation(Modulation):
    def __init__(
        self,
        bandwidth: float = None,
        baseband_bandwidth: float = None,
        carrier_to_noise: float = None,
        signal_to_noise: float = None,
        deviation_ratio: float = None,
        frequency_deviation: float = None,
        threshold: float = None,
        link_margin: float = None,
        deemphasis_improvement: float = 1,
        preemphasis_improvement: float = 1,
    ):
        """
        bandwidth (float, GHz): the range of frequencies required to transmit the signal
        baseband_bandwidth (float, GHz): the range of frequencies required to
            transmit the baseband signal
        carrier_to_noise (float, W):
        deemphasis_improvement (float, W):
        preemphasis_improvement (float, W):
        """
        self._bandwidth = bandwidth
        self._baseband_bandwidth = baseband_bandwidth
        self._carrier_to_noise = carrier_to_noise
        self._signal_to_noise = signal_to_noise
        self._deviation_ratio = deviation_ratio
        self._frequency_deviation = frequency_deviation
        self._deemphasis_improvement = deemphasis_improvement
        self._preemphasis_improvement = preemphasis_improvement
        self._threshold = threshold
        self._link_margin = link_margin

    @property
    def bandwidth(self) -> float:
        if self._bandwidth is None:
            self._bandwidth = 2 * (self.frequency_deviation + self.baseband_bandwidth)
        return self._bandwidth

    @property
    def frequency_deviation(self) -> float:
        if self._frequency_deviation is None:
            self._frequency_deviation = self.bandwidth / 2 - self.baseband_bandwidth
        return self._frequency_deviation

    @property
    def deviation_ratio(self) -> float:
        if self._deviation_ratio is None:
            self._deviation_ratio = self.frequency_deviation / self.baseband_bandwidth
        return self._deviation_ratio

    @property
    def signal_to_noise(self) -> float:
        if self._signal_to_noise is None:
            self._signal_to_noise = (
                (3 / 2)
                * self.carrier_to_noise
                * (self.bandwidth / self.baseband_bandwidth)
                * self.deviation_ratio**2
                * self.preemphasis_improvement
                * self.deemphasis_improvement
            )
        return self._signal_to_noise

    @property
    def link_margin(self) -> float:
        if self._link_margin is None:
            self._link_margin = self.carrier_to_noise / self.threshold
        return self._link_margin

    @property
    def threshold(self) -> float:
        return self._threshold

    @property
    def baseband_bandwidth(self) -> float:
        return self._baseband_bandwidth

    @property
    def carrier_to_noise(self) -> float:
        return self._carrier_to_noise

    @property
    def deemphasis_improvement(self) -> float:
        return self._deemphasis_improvement

    @property
    def preemphasis_improvement(self) -> float:
        return self._preemphasis_improvement


class Waveform:
    def __init__(
        self, frequency: float = None, amplitude: float = None, phase: float = None
    ):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase


class ConvolutionalCode:
    def __init__(self, coding_rate: float = None, coding_gain: float = None):
        """
        coding_rate (float, bps):
        coding_gain (float, W):
        """
        self._coding_rate = coding_rate
        self._coding_gain = coding_gain

    @property
    def coding_rate(self) -> float:
        return self._coding_rate

    @property
    def coding_gain(self) -> float:
        return self._coding_gain

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Coding Rate",
                    "unit": "mbps",
                    "value": self.coding_rate,
                },
                {
                    "name": "Coding Gain",
                    "unit": "dB",
                    "value": watt_to_decibel(self.coding_gain),
                },
            ]
        )
        summary.set_index("name", inplace=True)
        return summary


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
        bit_period: float = None,
        bits_per_symbol: int = None,
        carrier_power: float = None,
        coding_rate: float = None,
        carrier_to_noise: float = None,
        spectral_efficiency: float = None,
        eb_no: float = None,
        es_no: float = None,
        rolloff_rate: float = None,
        frequency_range: list = None,
        noise_probability: float = None,
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

    @property
    def es_no(self) -> float:
        if self._es_no is None:
            if self.carrier_to_noise is not None:
                self._es_no = (
                    self.carrier_to_noise * GHz_to_Hz(self.bandwidth) / self.symbol_rate
                )
            elif self.eb_no is not None:
                return self.eb_no * self.bits_per_symbol
        return self._es_no

    @property
    def eb_no(self) -> float:
        if self._eb_no is None:
            if self.bit_error_rate is not None:
                self._eb_no = (
                    erfcinv(self.bit_error_rate * self.bits_per_symbol)
                    / sin(pi / self.levels)
                ) ** 2 / self.bits_per_symbol
            elif self.es_no is not None:
                self._eb_no = self.es_no / self.bits_per_symbol
        return self._eb_no

    @property
    def carrier_power(self) -> float:
        return self._carrier_power

    @property
    def bit_rate(self) -> float:
        if self._bit_rate is None:
            if self.bit_period is not None:
                self._bit_rate = 1.0 / self.bit_period
            elif self.rolloff_rate is not None:
                self._bit_rate = (
                    self.bits_per_symbol
                    * GHz_to_Hz(self.bandwidth)
                    / (1 + self.rolloff_rate)
                )
        return self._bit_rate

    @property
    def data_rate(self) -> float:
        if self._data_rate is None:
            if self.code is not None:
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
            if self._bandwidth is not None and self._rolloff_rate is not None:
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
            self._spectral_efficiency = log2(self.levels) / (
                self.bandwidth * self.symbol_period
            )
        return self._spectral_efficiency

    @property
    def energy_per_symbol(self) -> float:
        if self._energy_per_symbol is None:
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
            self._energy_per_bit = self.carrier_power * self.bit_period
        return self._energy_per_bit

    @property
    def noise_power_density(self) -> float:
        if self._noise_power_density is None:
            self._noise_power_density = self.symbol_rate / (
                self.bandwidth * self.carrier_to_noise * self.energy_per_symbol
            )
        return self._noise_power_density

    @property
    def noise_probability(self) -> float:
        if self._noise_probability is None:
            self._noise_probability = erfc(
                sqrt(self.bits_per_symbol * self.eb_no) * sin(pi / self.levels)
            )
        return self._noise_probability

    @property
    def bit_error_rate(self) -> float:
        if self._bit_error_rate is None:
            if self.noise_probability is not None:
                self._bit_error_rate = self.noise_probability / self.bits_per_symbol
        return self._bit_error_rate

    @property
    def levels(self) -> float:
        return self._levels

    @property
    def rolloff_rate(self) -> float:
        return self._rolloff_rate

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_to_noise is None:
            if self.eb_no is not None:
                self._carrier_to_noise = (
                    self.eb_no * self.bit_rate / GHz_to_Hz(self._bandwidth)
                )
        return self._carrier_to_noise

    @property
    def carrier_signal(self) -> Waveform:
        return self._carrier_signal

    @property
    def code(self) -> ConvolutionalCode:
        return self._code

    @property
    def bandwidth(self) -> float:
        if self._bandwidth is None:
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
                    "unit": "bits/s/GHz",
                    "value": Hz_to_GHz(self.spectral_efficiency),
                },
                {
                    "name": "C/N Ratio",
                    "unit": "bits/s/GHz",
                    "value": watt_to_decibel(self.carrier_to_noise),
                },
                {
                    "name": "Eb/No Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.eb_no),
                },
                {
                    "name": "Bit Error Rate",
                    "unit": "",
                    "value": self.bit_error_rate,
                },
                {"name": "Roll-Off Factor", "unit": "", "value": self.rolloff_rate},
            ]
        )
        summary.set_index("name", inplace=True)

        if self.code is not None:
            code = self.code.summary()
            summary = pd.concat([summary, code])

        return summary


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
            self._noise_probability = 0.5 * erfc(sqrt(self.carrier_to_noise))
        return self._noise_probability


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
            self._noise_probability = 0.5 * erfc(sqrt(self.carrier_to_noise * 0.5))
        return self._noise_probability
