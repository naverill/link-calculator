import numpy as np

from link_calculator.conversions import decibel_to_watt, watt_to_decibel
from link_calculator.signal_processing.modulation import ConvolutionalCode


def test_coding_gain():
    eb_no_coded = decibel_to_watt(0.9)
    eb_no_uncoded = decibel_to_watt(8.8)
    assert np.isclose(
        watt_to_decibel(
            ConvolutionalCode.coding_gain_eb_no(eb_no_coded, eb_no_uncoded)
        ),
        8,
        rtol=0.2,
    )


def test_coding_gain_1():
    eb_no_coded = decibel_to_watt(3.7)
    eb_no_uncoded = decibel_to_watt(8.8)
    assert np.isclose(
        watt_to_decibel(
            ConvolutionalCode.coding_gain_eb_no(eb_no_coded, eb_no_uncoded)
        ),
        5,
        rtol=0.2,
    )


def test_coding_gain_2():
    eb_no_coded = decibel_to_watt(6.3)
    eb_no_uncoded = decibel_to_watt(8.8)
    assert np.isclose(
        watt_to_decibel(
            ConvolutionalCode.coding_gain_eb_no(eb_no_coded, eb_no_uncoded)
        ),
        2.5,
        rtol=0.2,
    )
