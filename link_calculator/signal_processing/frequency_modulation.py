import numpy as np

from link_calculator.signal_processing.modulation import Modulation


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
