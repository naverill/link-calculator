import numpy as np

from link_calculator.components.conversions import joules_to_decibel_joules
from link_calculator.components.modulation import (
    BinaryPhaseShiftKeying,
    FrequencyModulation,
    MPhaseShiftKeying,
    QuadraturePhaseShiftKeying,
    Waveform,
)
from link_calculator.propagation.conversions import decibel_to_watt, watt_to_decibel


def test_energy_per_bit():
    power = 1000  # W
    bit_rate = 50 * 1e6  # bps

    mod_scheme = MPhaseShiftKeying(levels=2, bit_rate=bit_rate, carrier_power=power)
    assert np.isclose(mod_scheme.bit_period, 0.02 * 1e-6, rtol=0.01)
    assert np.isclose(mod_scheme.symbol_rate, mod_scheme.bit_rate)
    assert np.isclose(mod_scheme.symbol_period, mod_scheme.bit_period)
    assert np.isclose(mod_scheme.energy_per_bit, 20 * 1e-6)
    assert np.isclose(
        joules_to_decibel_joules(mod_scheme.energy_per_bit), -47, rtol=0.01
    )


def test_fm_signal_to_noise():
    fm = FrequencyModulation(
        bandwidth=30 * 0.001,
        baseband_bandwidth=4.2 * 0.001,
        carrier_to_noise=decibel_to_watt(15),
        deemphasis_improvement=decibel_to_watt(9),
        preemphasis_improvement=decibel_to_watt(8),
    )
    assert np.isclose(watt_to_decibel(fm.signal_to_noise), 50.5, rtol=0.1)


def test_fm_link_margin():
    fm = FrequencyModulation(
        bandwidth=45 * 1e-6,
        baseband_bandwidth=3.4 * 1e-6,
        carrier_to_noise=decibel_to_watt(13),
        deemphasis_improvement=decibel_to_watt(2.5),
        preemphasis_improvement=decibel_to_watt(7 + 2.5),
        threshold=decibel_to_watt(6),
    )
    assert np.isclose(fm.frequency_deviation, 19.1 * 1e-6, rtol=0.1)
    assert np.isclose(watt_to_decibel(fm.signal_to_noise), 50.5, rtol=0.1)
    assert np.isclose(watt_to_decibel(fm.link_margin), 7, rtol=0.1)


def test_fm_test_frequency_deviation():
    fm = FrequencyModulation(bandwidth=25 * 1e-3, baseband_bandwidth=2 * 1e-3)
    assert np.isclose(fm.frequency_deviation * 1e3, 10.5)
    assert np.isclose(fm.deviation_ratio, 5.25)


def test_roll_off_factor():
    bandwidth = 1 * 0.001  # MHz to GHz
    rolloff_rate = 0.5
    mod = BinaryPhaseShiftKeying(bandwidth=bandwidth, rolloff_rate=rolloff_rate)
    assert np.isclose(mod.symbol_rate, 666.7 * 1e-6, rtol=0.01)


def test_bandwidth():
    carrier_power = 14.125
    symbol_rate = 16 * 0.001
    rolloff = 0.25
    wv = Waveform(frequency=14.125)

    mod = BinaryPhaseShiftKeying(
        carrier_power=carrier_power,
        carrier_signal=wv,
        symbol_rate=symbol_rate,
        rolloff_rate=rolloff,
    )
    assert np.isclose(mod.bandwidth, 20 * 0.001)
    fr = mod.frequency_range
    assert np.isclose(fr[0], 14.115)
    assert np.isclose(fr[1], 14.135)


def test_bandwidth_1():
    bit_rate = 45 * 0.001
    bits_per_symbol = 3
    levels = 2**bits_per_symbol
    rolloff_rate = 0.3

    mod = MPhaseShiftKeying(levels=levels, bit_rate=bit_rate, rolloff_rate=rolloff_rate)
    assert np.isclose(mod.bandwidth * 1000, 19.5)


def test_max_bit_rate():
    bandwidth = 36 * 0.001
    rolloff_rate = 0.4
    bmod = BinaryPhaseShiftKeying(bandwidth=bandwidth, rolloff_rate=rolloff_rate)
    assert np.isclose(bmod.bit_rate, 25.7 * 1e-3, rtol=0.01)
    qmod = QuadraturePhaseShiftKeying(bandwidth=bandwidth, rolloff_rate=rolloff_rate)
    assert np.isclose(qmod.bit_rate, 51.4 * 1e-3, rtol=0.01)


def test_max_bit_rate_1():
    bandwidth = 45 * 1e-3
    bits_per_symbol = 2
    levels = 2**bits_per_symbol
    rolloff_factor = 0.4

    mod = MPhaseShiftKeying(
        levels=levels, bandwidth=bandwidth, rolloff_rate=rolloff_factor
    )
    assert np.isclose(mod.bit_rate * 1000, 64.3, rtol=0.01)
