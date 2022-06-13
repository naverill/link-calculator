import numpy as np
import pandas as pd

from link_calculator.components.antennas import Amplifier, Antenna
from link_calculator.components.communicators import GroundStation, Satellite
from link_calculator.constants import BOLTZMANN_CONSTANT
from link_calculator.link_budget import Link, LinkBudget
from link_calculator.propagation.conversions import decibel_to_watt, watt_to_decibel
from link_calculator.signal_processing.conversions import MHz_to_GHz, mbit_to_bit
from link_calculator.signal_processing.modulation import MPhaseShiftKeying

pd.options.display.float_format = "{:,.2f}".format


def test_link_budget():
    psk = MPhaseShiftKeying(
        levels=8, bit_rate=mbit_to_bit(120), bandwidth=MHz_to_GHz(40)
    )
    # Ground Station
    gs_amp = Amplifier(
        power=decibel_to_watt(20), loss=decibel_to_watt(-3), gain=1  # back off loss
    )
    gs_transmit = Antenna(
        gain=decibel_to_watt(65),
        loss=decibel_to_watt(-3),  # feeder loss
        modulation=psk,
        amplifier=gs_amp,
    )
    gs_receive = Antenna(
        gain=1,
        loss=decibel_to_watt(-3),
        amplifier=gs_amp,
    )
    gs = GroundStation(
        name="gs",
        gain_to_equiv_noise_temp=decibel_to_watt(35.5),
        transmit=gs_transmit,
        receive=gs_receive,
    )

    # Satellite
    sat_amp = Amplifier(
        power=decibel_to_watt(10), loss=decibel_to_watt(-0.2), gain=1  # back-off loss
    )
    sat_transmit = Antenna(
        gain=decibel_to_watt(35),
        loss=decibel_to_watt(-0.5),  # feeder loss
        modulation=psk,
        amplifier=sat_amp,
    )
    sat_receive = Antenna(
        gain=1,
        loss=decibel_to_watt(-0.5),
        amplifier=sat_amp,
    )
    sat = Satellite(
        name="sat",
        transmit=sat_transmit,
        gain_to_equiv_noise_temp=decibel_to_watt(-5.5),
        receive=sat_receive,
    )
    uplink = Link(
        transmitter=gs,
        receiver=sat,
        atmospheric_loss=decibel_to_watt(-0.5),
        path_loss=decibel_to_watt(-206.4),  # 14 GHz
    )
    downlink = Link(
        transmitter=sat,
        receiver=gs,
        atmospheric_loss=decibel_to_watt(-0.3),
        path_loss=decibel_to_watt(-205.1),  # 12 GHz
    )

    budget = LinkBudget(uplink=uplink, downlink=downlink)

    """~~~~~~~~~~~~~~~~~~~ Uplink ~~~~~~~~~~~~~~~~~~~"""
    # Carrier to noise density
    assert np.isclose(
        watt_to_decibel(budget.uplink.transmitter.transmit.amplifier.power), 20
    )
    assert np.isclose(
        watt_to_decibel(budget.uplink.transmitter.transmit.amplifier.loss), -3
    )
    assert np.isclose(watt_to_decibel(budget.uplink.transmitter.transmit.gain), 65)
    assert np.isclose(watt_to_decibel(budget.uplink.transmitter.transmit.loss), -3)
    assert np.isclose(watt_to_decibel(budget.uplink.path_loss), -206.4)
    assert np.isclose(watt_to_decibel(budget.uplink.atmospheric_loss), -0.5)
    assert np.isclose(watt_to_decibel(BOLTZMANN_CONSTANT), -228.6, rtol=0.01)
    assert np.isclose(
        watt_to_decibel(budget.uplink.receiver.gain_to_equiv_noise_temp),
        -5.5,
        rtol=0.01,
    )
    assert np.isclose(
        watt_to_decibel(budget.uplink.transmitter.transmit.eirp), 79, rtol=0.01
    )
    assert np.isclose(
        watt_to_decibel(budget.uplink.carrier_to_noise_density), 94.7, rtol=0.01
    )

    # EbNo
    assert np.isclose(
        watt_to_decibel(budget.uplink.transmitter.transmit.modulation.bit_rate),
        80.79,
        rtol=0.01,
    )
    assert np.isclose(watt_to_decibel(budget.uplink.eb_no), 13.9, rtol=0.01)

    # carrier to noise
    assert np.isclose(
        budget.uplink.transmitter.transmit.modulation.bandwidth, 40e-3, rtol=0.01
    )
    assert np.isclose(
        budget.uplink.transmitter.transmit.modulation.bit_rate, 120e6, rtol=0.01
    )
    assert np.isclose(watt_to_decibel(budget.uplink.carrier_to_noise), 18.7, rtol=0.01)

    """~~~~~~~~~~~~~~~~~~~ downlink ~~~~~~~~~~~~~~~~~~~"""
    # Carrier to noise density
    assert np.isclose(
        watt_to_decibel(budget.downlink.transmitter.transmit.amplifier.power), 10
    )
    assert np.isclose(
        watt_to_decibel(budget.downlink.transmitter.transmit.amplifier.loss), -0.2
    )
    assert np.isclose(watt_to_decibel(budget.downlink.transmitter.transmit.gain), 35)
    assert np.isclose(watt_to_decibel(budget.downlink.transmitter.transmit.loss), -0.5)
    assert np.isclose(watt_to_decibel(budget.downlink.path_loss), -205.1)
    assert np.isclose(watt_to_decibel(budget.downlink.atmospheric_loss), -0.3)
    assert np.isclose(
        watt_to_decibel(budget.downlink.receiver.gain_to_equiv_noise_temp),
        35.5,
        rtol=0.01,
    )
    assert np.isclose(
        watt_to_decibel(budget.downlink.carrier_to_noise_density), 100, rtol=0.01
    )

    # EbNo
    assert np.isclose(
        watt_to_decibel(budget.downlink.transmitter.transmit.modulation.bit_rate),
        80.79,
        rtol=0.01,
    )
    assert np.isclose(watt_to_decibel(budget.downlink.eb_no), 19.21, rtol=0.01)

    # carrier to noise
    assert np.isclose(
        budget.downlink.transmitter.transmit.modulation.bandwidth, 40e-3, rtol=0.01
    )
    assert np.isclose(
        budget.downlink.transmitter.transmit.modulation.bit_rate, 120e6, rtol=0.01
    )
    assert np.isclose(
        watt_to_decibel(budget.downlink.carrier_to_noise), 23.98, rtol=0.01
    )

    """~~~~~~~~~~~~~~~~~~~ Link Budget ~~~~~~~~~~~~~~~~~~~"""
    assert np.isclose(watt_to_decibel(budget.eb_no), 12.8, rtol=0.01)
    print(budget.summary())
