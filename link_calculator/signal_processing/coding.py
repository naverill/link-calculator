from math import comb, factorial, log2, log10

import pandas as pd

from link_calculator.conversions import watt_to_decibel


class ConvolutionalCode:
    def __init__(
        self,
        coding_rate: float = None,
        coding_gain: float = None,
        min_distance: float = None,
    ):
        """
        coding_rate (float, bps):
        coding_gain (float, W):
        """
        self._coding_rate = coding_rate
        self._coding_gain = coding_gain
        self._min_distance = min_distance

    @property
    def coding_rate(self) -> float:
        return self._coding_rate

    @property
    def coding_gain(self) -> float:
        if self._coding_gain is None:
            if self._min_distance is not None:
                self._coding_gain = self.code_rate * self.min_distance
        return self._coding_gain

    @staticmethod
    def coding_gain_eb_no(eb_no_coded: float, eb_no_uncoded: float) -> float:
        """
        calculate the difference in Eb/No required to produce the same error rate for coded and
        uncoded signals

        Parameters
        ---------
            eb_no_coded (float, W); the Eb/No of the coded signal
            eb_no_coded (float, W): the Eb/No of the uncoded signal

        Returns
        -------
          coding_gain (float, ):
        """
        return eb_no_uncoded / eb_no_coded

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


def information_content(message_probability: float) -> float:
    """
    Calculate the information content of a message

    Parameters
    ----------
        message_probability (float, ): the probability  of occurrence of the message

    return
      information (float, bits)
    """
    return log2(1 / message_probability)


def total_information(message_probabilities: list[float]) -> float:
    """
    Total information in a set of M messages

    Parameters
    ----------
      message_probabilities (list, ): proability of occurence of a set of messages
    Return
    ------
        total_info (float, bits)
    """
    M = len(message_probabilities)
    return M * sum([prob * information_content(prob) for prob in message_probabilities])


def entropy(message_probabilities: list[float]) -> float:
    """
    Average information content per message

    Parameters
    ----------
      message_probabilities (list, ): proability of occurence of a set of messages
    Return
    ------
        entropy (float, bits per message)
    """
    M = len(message_probabilities)
    return total_information(message_probabilities) / M


def average_information_rate(
    n_transmitted: int, message_probabilities: list[float]
) -> float:
    """
    Average information rate per second

    Parameters
    ----------
      n_transmitted (int, ): number of messages send per second
      message_probabilities (list, ): proability of occurence of a set of messages
    Return
    ------
        average information rate (float, bits per second)
    """
    return n_transmitted * entropy(message_probabilities)


def error_probability(block_size, n_errors, error_probability) -> float:
    return (
        comb(block_size, n_errors)
        * (error_probability**n_errors)
        * (1 - error_probability) ** (block_size - n_errors)
    )
