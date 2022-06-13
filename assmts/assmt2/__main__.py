import numpy as np
import pandas as pd

from link_calculator.components.antennas import Amplifier, ParabolicAntenna
from link_calculator.components.communicators import GroundStation, Satellite
from link_calculator.constants import BOLTZMANN_CONSTANT
from link_calculator.link_budget import Link, LinkBudget
from link_calculator.orbits.utils import GeodeticCoordinate, Orbit
from link_calculator.propagation.conversions import decibel_to_watt, watt_to_decibel
from link_calculator.signal_processing.conversions import (
    MHz_to_GHz,
    MHz_to_Hz,
    mbit_to_bit,
)
from link_calculator.signal_processing.modulation import MPhaseShiftKeying

print("\n\n")

pd.options.display.float_format = "{:,.2f}".format


def q1():
    sat_mod = MPhaseShiftKeying(levels=8, bandwidth=MHz_to_GHz(50), rolloff_rate=0.3)

    # Ground Station A
    gsA_point = GeodeticCoordinate(latitude=-19.08, longitude=178.18)
    gsA_amp = Amplifier(
        power=40,
    )
    gsA_transmit = ParabolicAntenna(
        frequency=30.5,
        efficiency=0.55,
        circular_diameter=1.2,
        loss=decibel_to_watt(-1),
        amplifier=gsA_amp,
        modulation=sat_mod,
    )
    gsA_receive = ParabolicAntenna(
        frequency=20.5,
        efficiency=0.55,
        circular_diameter=1.2,
        loss=decibel_to_watt(-1),
        amplifier=gsA_amp,
        modulation=sat_mod,
    )
    gsA = GroundStation(
        name="EarthStationA",
        noise_figure=2.8,
        noise_temperature=25.0,
        ground_coordinate=gsA_point,
        transmit=gsA_transmit,
        receive=gsA_receive,
    )

    # Ground Station B
    gsB_point = GeodeticCoordinate(latitude=-19.08, longitude=178.18)
    gsB_amp = Amplifier(
        power=80,
    )
    gsB_transmit = ParabolicAntenna(
        frequency=30.5,
        circular_diameter=0.8,
        efficiency=0.6,
        loss=decibel_to_watt(-1.0),
        amplifier=gsB_amp,
        modulation=sat_mod,
    )
    gsB_receive = ParabolicAntenna(
        frequency=20.5,
        circular_diameter=0.8,
        efficiency=0.6,
        loss=decibel_to_watt(-1.0),
        amplifier=gsB_amp,
        modulation=sat_mod,
    )
    gsB = GroundStation(
        name="EarthStationB",
        noise_figure=2.5,
        noise_temperature=25.0,
        ground_coordinate=gsB_point,
        transmit=gsB_transmit,
        receive=gsB_receive,
    )

    # Ground Station F
    gsF_point = GeodeticCoordinate(latitude=-35.17, longitude=147.27)
    gsF_amp = Amplifier(
        power=500.0,
    )
    gsF_transmit = ParabolicAntenna(
        frequency=30.5,
        circular_diameter=10.5,
        efficiency=0.65,
        loss=decibel_to_watt(-2.5),
        amplifier=gsF_amp,
        modulation=sat_mod,
    )
    gsF_receive = ParabolicAntenna(
        frequency=20.5,
        circular_diameter=10.5,
        efficiency=0.65,
        loss=decibel_to_watt(-2.5),
        amplifier=gsF_amp,
        modulation=sat_mod,
    )
    gsF = GroundStation(
        name="EarthStationFixed",
        noise_figure=2.1,
        noise_temperature=25.0,
        transmit=gsF_transmit,
        receive=gsF_receive,
        ground_coordinate=gsF_point,
    )

    # Satellite
    orbit = Orbit(orbital_radius=42164)
    ss_point = GeodeticCoordinate(latitude=0, longitude=149.8)
    sat_amp = Amplifier(
        power=8.0,
    )
    sat_transmit = ParabolicAntenna(
        frequency=20.5,  # GHz
        modulation=sat_mod,
        amplifier=sat_amp,
        circular_diameter=1.0,
        efficiency=0.6,
        loss=decibel_to_watt(-0.5),
    )
    sat_receive = ParabolicAntenna(
        frequency=30.5,  # GHz
        modulation=sat_mod,
        amplifier=sat_amp,
        circular_diameter=1.0,
        efficiency=0.6,
        loss=decibel_to_watt(-0.5),
    )
    sat = Satellite(
        name="sat",
        noise_temperature=300,
        noise_figure=2.5,
        transmit=sat_transmit,
        receive=sat_receive,
        ground_coordinate=ss_point,
        orbit=orbit,
    )

    gsA_uplink_upstream = Link(
        transmitter=gsA,
        receiver=sat,
        atmospheric_loss=decibel_to_watt(-6.0),
        slant_range=Link.distance(sat, gsA),
    )
    gsA_downlink_upstream = Link(
        slant_range=Link.distance(sat, gsF),
        transmitter=sat,
        receiver=gsF,
        atmospheric_loss=decibel_to_watt(-6.0),
    )
    gsA_upstream_budget = LinkBudget(
        uplink=gsA_uplink_upstream, downlink=gsA_downlink_upstream
    )
    gsA_upstream_summary = gsA_upstream_budget.summary()
    gsA_upstream_summary.rename(
        columns={"name": "Earth Station A Upstream"}, inplace=True
    )
    gsA_upstream_summary.to_csv("Earth Station A Upstream.csv")

    gsA_uplink_downstream = Link(
        transmitter=gsF,
        receiver=sat,
        atmospheric_loss=decibel_to_watt(-6.0),
        slant_range=Link.distance(sat, gsF),
    )
    gsA_downlink_downstream = Link(
        slant_range=Link.distance(sat, gsA),
        transmitter=sat,
        receiver=gsA,
        atmospheric_loss=decibel_to_watt(-6.0),
    )
    gsA_downstream_budget = LinkBudget(
        uplink=gsA_uplink_downstream, downlink=gsA_downlink_downstream
    )
    gsA_downstream_summary = gsA_downstream_budget.summary()
    gsA_downstream_summary.rename(
        columns={"name": "Earth Station A Downstream"}, inplace=True
    )
    gsA_downstream_summary.to_csv("Earth Station A Downstream.csv")

    gsB_uplink_upstream = Link(
        transmitter=gsB,
        receiver=sat,
        atmospheric_loss=decibel_to_watt(-6.0),
        slant_range=Link.distance(sat, gsB),
    )
    gsB_downlink_upstream = Link(
        slant_range=Link.distance(sat, gsF),
        transmitter=sat,
        receiver=gsF,
        atmospheric_loss=decibel_to_watt(-6.0),
    )
    gsB_upstream_budget = LinkBudget(
        uplink=gsB_uplink_upstream, downlink=gsB_downlink_upstream
    )
    gsB_upstream_summary = gsB_upstream_budget.summary()
    gsB_upstream_summary.rename(
        columns={"name": "Earth Station B Upstream"}, inplace=True
    )
    gsB_upstream_summary.to_csv("Earth Station B Upstream.csv")

    gsB_uplink_downstream = Link(
        transmitter=gsF,
        receiver=sat,
        atmospheric_loss=decibel_to_watt(-6.0),
        slant_range=Link.distance(sat, gsF),
    )
    gsB_downlink_downstream = Link(
        slant_range=Link.distance(sat, gsB),
        transmitter=sat,
        receiver=gsB,
        atmospheric_loss=decibel_to_watt(-6.0),
    )
    gsB_downstream_budget = LinkBudget(
        uplink=gsB_uplink_downstream, downlink=gsB_downlink_downstream
    )
    gsB_downstream_summary = gsB_downstream_budget.summary()
    gsB_downstream_summary.rename(
        columns={"name": "Earth Station B Downstream"}, inplace=True
    )
    gsB_downstream_summary.to_csv("Earth Station B Downstream.csv")


def q2():
    pass


def q3():
    pass


q1()
q2()
q3()
