import numpy as np

from link_calculator.conversions import (
    GHz_to_Hz,
    GHz_to_MHz,
    Hz_to_MHz,
    MHz_to_GHz,
    bit_to_mbit,
    decibel_to_watt,
    joules_to_decibel_joules,
    mbit_to_bit,
    watt_to_decibel,
)
from link_calculator.signal_processing.frequency_modulation import FrequencyModulation
from link_calculator.signal_processing.modulation import (
    BinaryPhaseShiftKeying,
    MPhaseShiftKeying,
    QuadraturePhaseShiftKeying,
    Waveform,
)


def test_ber_to_eb_no():
    min_bit_error_rate = 1e-9
    mod = MPhaseShiftKeying(
        levels=8,
        bit_error_rate=min_bit_error_rate,
        bandwidth=MHz_to_GHz(50),
        rolloff_rate=0.3,
    )
    conv_eb_no = mod.eb_no

    conv_mod = MPhaseShiftKeying(
        levels=8, bandwidth=MHz_to_GHz(50), rolloff_rate=0.3, eb_no=conv_eb_no
    )
    assert np.isclose(conv_mod.bit_error_rate, mod.bit_error_rate, rtol=0.01)


def test_eb_no_to_ber():
    mod = MPhaseShiftKeying(
        levels=8,
        bandwidth=MHz_to_GHz(50),
        rolloff_rate=0.3,
        eb_no=decibel_to_watt(22.5),
    )
    conv_eb_no = mod.eb_no
    conv_mod = MPhaseShiftKeying(
        levels=8,
        eb_no=conv_eb_no,
        bandwidth=MHz_to_GHz(50),
        rolloff_rate=0.3,
    )

    assert np.isclose(conv_mod.eb_no, mod.eb_no, rtol=0.01)


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
    fm = FrequencyModulation(bandwidth=MHz_to_GHz(25), baseband_bandwidth=MHz_to_GHz(2))
    assert np.isclose(GHz_to_MHz(fm.frequency_deviation), 10.5)
    assert np.isclose(fm.deviation_ratio, 5.25)


def test_fm_frequency_deviation_1():
    fm = FrequencyModulation(
        bandwidth=MHz_to_GHz(35),
        baseband_bandwidth=MHz_to_GHz(5),
    )
    assert np.isclose(GHz_to_MHz(fm.frequency_deviation), 12.5, rtol=0.01)
    assert np.isclose(fm.deviation_ratio, 2.5, rtol=0.01)


def test_roll_off_factor():
    bandwidth = MHz_to_GHz(1)  # MHz to GHz
    rolloff_rate = 0.5
    mod = BinaryPhaseShiftKeying(bandwidth=bandwidth, rolloff_rate=rolloff_rate)
    assert np.isclose(bit_to_mbit(mod.symbol_rate), 666.7 * 1e-3, rtol=0.01)


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


def test_bandwidth_2():
    bit_rate = 50 * 1e-3
    bits_per_symbol = 2
    levels = 2**bits_per_symbol
    rolloff_factor = 0.3

    mod = MPhaseShiftKeying(
        levels=levels, bit_rate=bit_rate, rolloff_rate=rolloff_factor
    )
    assert np.isclose(GHz_to_MHz(mod.bandwidth), 32.5, rtol=0.01)


def test_max_bit_rate():
    bandwidth = MHz_to_GHz(36)
    rolloff_rate = 0.4
    bmod = BinaryPhaseShiftKeying(bandwidth=bandwidth, rolloff_rate=rolloff_rate)
    assert np.isclose(bit_to_mbit(bmod.bit_rate), 25.7, rtol=0.01)
    qmod = QuadraturePhaseShiftKeying(bandwidth=bandwidth, rolloff_rate=rolloff_rate)
    assert np.isclose(bit_to_mbit(qmod.bit_rate), 51.4, rtol=0.01)


def test_max_bit_rate_1():
    bandwidth = MHz_to_GHz(45)
    bits_per_symbol = 2
    levels = 2**bits_per_symbol
    rolloff_factor = 0.4

    mod = MPhaseShiftKeying(
        levels=levels, bandwidth=bandwidth, rolloff_rate=rolloff_factor
    )
    assert np.isclose(bit_to_mbit(mod.bit_rate), 64.3, rtol=0.01)


def test_max_bit_rate_2():
    bandwidth = MHz_to_GHz(35)
    bits_per_symbol = 3
    levels = 2**bits_per_symbol
    rolloff_factor = 0.3

    mod = MPhaseShiftKeying(
        levels=levels, bandwidth=bandwidth, rolloff_rate=rolloff_factor
    )
    assert np.isclose(bit_to_mbit(mod.bit_rate), 80.8, rtol=0.01)


def test_max_bit_rate_3():
    bandwidth = MHz_to_GHz(35)
    bits_per_symbol = 4
    levels = 2**bits_per_symbol
    rolloff_factor = 0.3

    mod = MPhaseShiftKeying(
        levels=levels, bandwidth=bandwidth, rolloff_rate=rolloff_factor
    )
    assert np.isclose(bit_to_mbit(mod.bit_rate), 107.7, rtol=0.01)


def test_eb_no():
    bandwidth = MHz_to_GHz(35)
    bits_per_symbol = 4
    levels = 2**bits_per_symbol
    rolloff_factor = 0.3
    carrier_to_noise = decibel_to_watt(23.9)

    mod = MPhaseShiftKeying(
        levels=levels,
        bandwidth=bandwidth,
        rolloff_rate=rolloff_factor,
        carrier_to_noise=carrier_to_noise,
    )
    assert np.isclose(watt_to_decibel(mod.eb_no), 19.02, rtol=0.01)
