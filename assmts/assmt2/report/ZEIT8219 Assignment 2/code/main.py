import pathlib
from math import inf, pi

import numpy as np
import pandas as pd

from link_calculator.components.antennas import Amplifier, Antenna, ParabolicAntenna
from link_calculator.components.communicators import GroundStation, Satellite
from link_calculator.constants import BOLTZMANN_CONSTANT, EARTH_RADIUS
from link_calculator.link_budget import Link, LinkBudget
from link_calculator.orbits.utils import GeodeticCoordinate, Orbit
from link_calculator.propagation.conversions import decibel_to_watt, watt_to_decibel
from link_calculator.signal_processing.conversions import (
    Hz_to_GHz,
    MHz_to_GHz,
    MHz_to_Hz,
    mbit_to_bit,
)
from link_calculator.signal_processing.modulation import (
    ConvolutionalCode,
    MPhaseShiftKeying,
)

print("\n\n")

ABS_PATH = pathlib.Path(__file__).parent.resolve()


def q1():
    sat_mod = MPhaseShiftKeying(
        levels=8,
        bandwidth=MHz_to_GHz(50),
        rolloff_rate=0.3,
    )

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
    gsA_upstream_summary.index = (
        gsA_upstream_summary.index + " (" + gsA_upstream_summary.pop("unit") + ")"
    )
    gsA_upstream_summary.to_csv(
        f"{ABS_PATH}/output/Q1EarthStationAUpstream.csv", float_format="{:,.3f}".format
    )
    print(gsA_upstream_summary)

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
    gsA_downstream_summary.index = (
        gsA_downstream_summary.index + " (" + gsA_downstream_summary.pop("unit") + ")"
    )
    gsA_downstream_summary.to_csv(
        f"{ABS_PATH}/output/Q1EarthStationADownstream.csv",
        float_format="{:,.3f}".format,
    )
    print(gsA_downstream_summary)

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
    gsB_upstream_summary.index = (
        gsB_upstream_summary.index + " (" + gsB_upstream_summary.pop("unit") + ")"
    )
    gsB_upstream_summary.to_csv(
        f"{ABS_PATH}/output/Q1EarthStationBUpstream.csv", float_format="{:,.3f}".format
    )
    print(gsB_upstream_summary)

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
    gsB_downstream_summary.index = (
        gsB_downstream_summary.index + " (" + gsB_downstream_summary.pop("unit") + ")"
    )
    gsB_downstream_summary.to_csv(
        f"{ABS_PATH}/output/Q1EarthStationBDownstream.csv",
        float_format="{:,.3f}".format,
    )


def q2():
    def link_eb_no(overall_eb_no: float, link_eb_no) -> float:
        return (overall_eb_no * link_eb_no) / (link_eb_no - overall_eb_no)

    uplink_eb_no = decibel_to_watt(33.2)
    min_bit_error_rate = 1e-9
    min_data_rate = mbit_to_bit(60)

    codes = {
        "7-8": {"code_rate": 7 / 8, "code_gain": decibel_to_watt(2.5)},
        "3-4": {"code_rate": 3 / 4, "code_gain": decibel_to_watt(3)},
        "1-2": {"code_rate": 1 / 2, "code_gain": decibel_to_watt(3.5)},
    }
    results = {}
    for name, params in codes.items():
        print(decibel_to_watt(params["code_gain"]))
        code = ConvolutionalCode(
            coding_rate=params["code_rate"], coding_gain=params["code_gain"]
        )
        mod = MPhaseShiftKeying(
            levels=8,
            bandwidth=MHz_to_GHz(50),
            rolloff_rate=0.3,
            code=code,
            eb_no=uplink_eb_no,
        )
        results[name] = {"data_rate": mod.data_rate, "mod": mod}
        summary = mod.summary()
        summary.rename(columns={"name": f"{name} Modulation Summary"}, inplace=True)
        print(summary)
        summary.index = summary.index + " (" + summary.pop("unit") + ")"
        summary.to_csv(
            f"{ABS_PATH}/output/Q2{name}Modulation.csv", float_format="{:,.3f}".format
        )

    best_code = min(
        results,
        key=lambda x: results[x]["data_rate"]
        if results[x]["data_rate"] > min_data_rate
        else inf,
    )
    best_mod = results[best_code]["mod"]

    overall_mod = MPhaseShiftKeying(
        levels=8,
        bit_error_rate=min_bit_error_rate,
        bandwidth=MHz_to_GHz(50),
        rolloff_rate=0.3,
        code=best_mod.code,
    )
    overall_summary = overall_mod.summary()
    overall_summary.rename(
        columns={"name": "Overall Link Modulation Summary"}, inplace=True
    )
    overall_summary.index = (
        overall_summary.index + " (" + overall_summary.pop("unit") + ")"
    )
    print(overall_summary)
    overall_summary.to_csv(
        f"{ABS_PATH}/output/Q2OverallModulation.csv", float_format="{:,.3f}".format
    )

    downlink_eb_no = link_eb_no(overall_mod.eb_no, uplink_eb_no)
    downlink_mod = MPhaseShiftKeying(
        levels=8,
        bandwidth=MHz_to_GHz(50),
        eb_no=downlink_eb_no,
        rolloff_rate=0.3,
        code=best_mod.code,
    )
    downlink_summary = downlink_mod.summary()
    downlink_summary.index = (
        downlink_summary.index + " (" + downlink_summary.pop("unit") + ")"
    )
    print(downlink_summary)
    downlink_summary.to_csv(
        f"{ABS_PATH}/output/Q2DownlinkModulation.csv", float_format="{:,.3f}".format
    )


def inches_to_m(value) -> float:
    return 0.0254 * value


def q3():
    """
    TODO
        - finalise parameters
            - bit error rate
        - add signal to noise to output
    """
    locs = {
        "LowAltitudeOperations": GeodeticCoordinate(
            latitude=-3.74603, longitude=124.401, altitude=0
        ),  # 15000km outside of RAAF Base Tindal
        "HighAltitudeOperations": GeodeticCoordinate(
            latitude=-3.74603, longitude=124.401, altitude=17
        ),
    }

    for scenario, uav_loc in locs.items():
        code = ConvolutionalCode(coding_rate=3 / 4, coding_gain=decibel_to_watt(6.5))
        triton_transmit_mod = MPhaseShiftKeying(
            levels=4,
            bandwidth=MHz_to_GHz(50),
            bit_rate=mbit_to_bit(400),
            spectral_efficiency=4,  # bit/s/Hz
            bit_error_rate=1e-6,
            code=code,
            rolloff_rate=0.4,
        )
        triton_transmit_amp = Amplifier(power=35, loss=decibel_to_watt(-1))
        triton_transmit = Antenna(
            eirp=decibel_to_watt(55.5),
            cross_sect_area=inches_to_m(24.2) * inches_to_m(22.4),
            amplifier=triton_transmit_amp,
            frequency=29,
            modulation=triton_transmit_mod,
            loss=decibel_to_watt(-6),
        )
        triton_receive_mod = MPhaseShiftKeying(
            levels=4,
            bandwidth=MHz_to_GHz(100),
            bit_rate=mbit_to_bit(200),
            spectral_efficiency=4,  # bit/s/Hz
            bit_error_rate=1e-5,
            code=code,
            rolloff_rate=0.4,
        )
        triton_receive_amp = Amplifier(power=35, loss=decibel_to_watt(-1))
        triton_receive = Antenna(
            eirp=decibel_to_watt(55.5),
            cross_sect_area=inches_to_m(30.6) * inches_to_m(32.4),
            amplifier=triton_receive_amp,
            frequency=19,
            modulation=triton_receive_mod,
            loss=decibel_to_watt(-6),
        )
        triton = GroundStation(
            name="MQ-4C Triton",
            transmit=triton_transmit,
            receive=triton_receive,
            ground_coordinate=uav_loc,
        )

        ss_point = GeodeticCoordinate(latitude=-3.74603, longitude=124.401, altitude=16)
        kuiper_transmit_mod = MPhaseShiftKeying(
            levels=4,
            bandwidth=MHz_to_GHz(100),
            bit_error_rate=1e-5,
            bit_rate=mbit_to_bit(200),
            code=code,
            rolloff_rate=0.4,
        )
        kuiper_transmit_amp = Amplifier(
            power=38.7,
            loss=decibel_to_watt(-1),
        )
        kuiper_transmit = Antenna(
            cross_sect_area=pi * 1.6**2,
            eirp=decibel_to_watt(35.8),
            modulation=kuiper_transmit_mod,
            gain=decibel_to_watt(37),
            frequency=19,
            amplifier=kuiper_transmit_amp,
            loss=decibel_to_watt(-6),
        )
        kuiper_receive_mod = MPhaseShiftKeying(
            levels=4,
            bit_rate=mbit_to_bit(400),
            bit_error_rate=1e-6,
            bandwidth=MHz_to_GHz(50),
            code=code,
            rolloff_rate=0.4,
        )
        kuiper_receive_amp = Amplifier(
            power=38.7,
            loss=decibel_to_watt(-1),
        )
        kuiper_receive = Antenna(
            cross_sect_area=pi * 1.6**2,
            eirp=decibel_to_watt(46.0),
            gain=decibel_to_watt(37),
            loss=decibel_to_watt(-6),
            frequency=29,
            modulation=kuiper_receive_mod,
            amplifier=kuiper_receive_amp,
        )
        orbit = Orbit(orbital_radius=630 + EARTH_RADIUS)
        kuiper = Satellite(
            name="KuiperSat-1",
            orbit=orbit,
            transmit=kuiper_transmit,
            receive=kuiper_receive,
            ground_coordinate=ss_point,
        )

        uplink = Link(
            transmitter=triton,
            receiver=kuiper,
            atmospheric_loss=decibel_to_watt(-84.0),
            slant_range=Link.distance(kuiper, triton)
            - triton.ground_coordinate.altitude,
            #            eb_no=decibel_to_watt(10.5),
        )
        downlink = Link(
            transmitter=kuiper,
            receiver=triton,
            atmospheric_loss=decibel_to_watt(-84.0),
            slant_range=Link.distance(kuiper, triton)
            - triton.ground_coordinate.altitude,
            #           eb_no=decibel_to_watt(10.5),
        )
        link_budget = LinkBudget(uplink=uplink, downlink=downlink)
        link_summary = link_budget.summary()
        link_summary.index = link_summary.index + " (" + link_summary.pop("unit") + ")"
        link_summary.to_csv(
            f"{ABS_PATH}/output/Q3Tritan{scenario}.csv", float_format="{:,.3f}".format
        )
        print(link_summary)


q1()
q2()
q3()
