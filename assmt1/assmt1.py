import numpy as np
import pandas as pd

from link_calculator.components import Antenna, GroundStation, Satellite
from link_calculator.orbits.utils import (
    angle_sat_to_ground_station,
    elevation_angle,
    slant_range,
)
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
)
from link_calculator.propagation.utils import receive_power


def load_gmat_report(file_path):
    return pd.read_csv(file_path, sep="\s{1,}", engine="python")


def q2(
    report: pd.DataFrame, satellites: list[str], ground_stations: list[GroundStation]
):
    for sat in satellites:
        for gs in ground_stations:
            report[f"{sat.name}.Earth.Gamma.{gs.name}"] = report.apply(
                lambda row: angle_sat_to_ground_station(
                    gs.latitude,
                    gs.longitude,
                    row[f"{sat.name}.Earth.Latitude"],
                    row[f"{sat.name}.Earth.Longitude"],
                ),
                axis=1,
            )
            report[f"{sat.name}.Earth.SlantRange.{gs.name}"] = report.apply(
                lambda row: slant_range(
                    row[f"{sat.name}.Earth.RMAG"],
                    row[f"{sat.name}.Earth.Gamma.{gs.name}"],
                ),
                axis=1,
            )
            report[f"{sat.name}.Earth.Elevation.{gs.name}"] = report.apply(
                lambda row: elevation_angle(
                    row[f"{sat.name}.Earth.RMAG"],
                    row[f"{sat.name}.Earth.Gamma.{gs.name}"],
                ),
                axis=1,
            )

    min_elevation = 20
    for gs in ground_stations:
        assert all(
            np.logical_or.reduce(
                [
                    report[f"{sat.name}.Earth.Elevation.{gs.name}"] > min_elevation
                    for sat in satellites
                ]
            )
        )
    return report


def q3(
    report: pd.DataFrame,
    satellites: list[str],
    ground_stations: list[GroundStation],
):
    for gs in ground_stations:
        for sat in satellites:
            report[f"{sat.name}.Earth.ReceivePower.{gs.name}"] = report.apply(
                lambda row: receive_power(
                    sat.antenna.power,
                    sat.antenna.loss,
                    sat.antenna.gain,
                    row[f"{sat.name}.Earth.SlantRange.{gs.name}"],
                    gs.antenna.loss,
                    gs.antenna.gain,
                    1,
                    wavelength=frequency_to_wavelength(sat.antenna.frequency),
                )
                if row[f"{sat.name}.Earth.Elevation.{gs.name}"] > 20
                else None,
                axis=1,
            )
    return report


if __name__ == "__main__":
    # ka_band = 26.5–40 GHz
    sat_frequency = 20
    gs_frequency = 30
    ground_stations = [
        GroundStation(
            "CocosIsland",
            -12.167,
            96.833,
            0,
            Antenna("CocosReceive", 0, decibel_to_watt(18), 1, gs_frequency),
        ),
        GroundStation(
            "MawsonResearchStation",
            -67.6,
            62.867,
            0,
            Antenna("MawsonReceive", 0, decibel_to_watt(18), 1, gs_frequency),
        ),
        GroundStation(
            "NorfolkIsland",
            -29.033,
            167.95,
            0,
            Antenna("MawsonReceive", 0, decibel_to_watt(18), 1, gs_frequency),
        ),
    ]

    satellites = [
        Satellite(
            "GEO1", Antenna("GEO1Transmit", 5, decibel_to_watt(30), 1, sat_frequency)
        ),
        Satellite(
            "GEO2", Antenna("GEO2Transmit", 5, decibel_to_watt(30), 1, sat_frequency)
        ),
        Satellite(
            "GEO3", Antenna("GEO3Transmit", 5, decibel_to_watt(30), 1, sat_frequency)
        ),
    ]

    report = load_gmat_report("data/OrbitParams.txt")
    report = q2(report, satellites, ground_stations)
    report = q3(report, satellites, ground_stations)
    report.to_csv("output/report.csv")
