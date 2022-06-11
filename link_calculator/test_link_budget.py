import numpy as np

from link_calculator.components.antennas import Amplifier, Antenna
from link_calculator.components.communicators import GroundStation, Satellite
from link_calculator.link_budget import Link, LinkBudget
from link_calculator.propagation.conversions import decibel_to_watt, watt_to_decibel
from link_calculator.signal_processing.conversions import MHz_to_GHz
from link_calculator.signal_processing.modulation import MPhaseShiftKeying


def test_link_budget():
    psk = MPhaseShiftKeying(levels=8, bit_rate=120, bandwidth=MHz_to_GHz(40))
    # Ground Station
    gs_transmit = Antenna(
        power=decibel_to_watt(30),
        gain=decibel_to_watt(65),
        loss=decibel_to_watt(3),  # feeder loss
        modulation=psk,
    )
    gs_receive = Antenna(loss=decibel_to_watt(3))
    gs_amp = Amplifier(
        loss=decibel_to_watt(3),  # back off loss
    )
    gs = GroundStation(
        name="gs",
        gain_to_equiv_noise_temp=decibel_to_watt(-5.5),
        transmit=gs_transmit,
        receive=gs_receive,
        amplifier=gs_amp,
    )

    # Satellite
    sat_amp = Amplifier(
        loss=decibel_to_watt(0.2),  # back-off loss
    )
    sat_transmit = Antenna(
        power=decibel_to_watt(10),
        gain=decibel_to_watt(35),
        loss=decibel_to_watt(0.5),  # feeder loss
        modulation=psk,
    )
    sat_receive = Antenna(loss=decibel_to_watt(0.5))
    sat = Satellite(
        name="sat",
        gain_to_equiv_noise_temp=decibel_to_watt(-5.5),
        transmit=sat_transmit,
        receive=sat_receive,
        amplifier=sat_amp,
    )
    distance = Link.distance(sat, gs)
    uplink = Link(
        transmitter=gs,
        receiver=sat,
        atmospheric_loss=watt_to_decibel(0.5),
        path_loss=decibel_to_watt(206.4),  # 14 GHz
        distance=distance,
    )
    downlink = Link(
        transmitter=sat,
        receiver=gs,
        atmospheric_loss=-watt_to_decibel(0.3),
        path_loss=decibel_to_watt(205.1),  # 12 GHz
        distance=distance,
    )

    budget = LinkBudget(uplink=uplink, downlink=downlink)
    assert np.isclose(
        watt_to_decibel(budget.uplink.carrier_to_noise_density), 104.5, rtol=0.01
    )
    assert np.isclose(watt_to_decibel(budget.uplink.eb_no), 23.71, rtol=0.01)
    assert np.isclose(
        watt_to_decibel(budget.uplink.carrier_to_noise), 28.4812, rtol=0.01
    )

    assert np.isclose(
        watt_to_decibel(budget.downlink.carrier_to_noise_density), 100, rtol=0.01
    )
    assert np.isclose(watt_to_decibel(budget.downlink.eb_no), 19.21, rtol=0.01)
    assert np.isclose(
        watt_to_decibel(budget.downlink.carrier_to_noise), 23.9812, rtol=0.01
    )
    assert np.isclose(watt_to_decibel(budget.eb_no), 17.89, rtol=0.01)
