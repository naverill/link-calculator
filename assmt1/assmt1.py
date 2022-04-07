import numpy as np
import pandas as pd

from link_calculator.ground_station import Antenna, GroundStation, Satellite
from link_calculator.orbits.utils import (
    angle_sat_to_ground_station,
    elevation_angle,
    slant_range,
)
from link_calculator.propagation.conversions import decibel_to_watt


def load_gmat_report(file_path):
    return pd.read_csv(file_path, sep="\s{1,}")


def q2(
    report: pd.DataFrame, satellites: list[str], ground_stations: list[GroundStation]
):
    for sat in satellites:
        for gs in ground_stations:
            report[f"{sat.name}.Gamma.{gs.name}"] = report.apply(
                lambda row: angle_sat_to_ground_station(
                    gs.latitude,
                    gs.longitude,
                    row[f"{sat.name}.Latitude"],
                    row[f"{sat.name}.Longitude"],
                ),
                axis=1,
            )
            report[f"{sat.name}.SlantRange.{gs.name}"] = report.apply(
                lambda row: slant_range(
                    row[f"{sat.name}.RMAG"], row[f"{sat.name}.Gamma.{gs.name}"]
                ),
                axis=1,
            )
            report[f"{sat.name}.Elevation.{gs.name}"] = report.apply(
                lambda row: elevation_angle(
                    row[f"{sat.name}.RMAG"], row[f"{sat.name}.Gamma.{gs.name}"]
                ),
                axis=1,
            )

    min_elevation = 20
    for gs in ground_stations:
        assert all(
            np.logical_or.reduce(
                (
                    report[f"{sat.name}.Elevation.{gs.name}"] > min_elevation
                    for sat in satellites
                )
            )
        )
    return report


def q3(
    report: pd.DataFrame,
    Antenna,
    satellites: list[str],
    ground_stations: list[GroundStation],
):
    return


if __name__ == "__main__":
    ground_stations = [
        GroundStation(
            "CocosIsland", -12.167, 96.833, 0, Antenna(0, decibel_to_watt(18), 1)
        ),
        GroundStation(
            "MawsonResearchStation",
            -67.6,
            62.867,
            0,
            Antenna(0, decibel_to_watt(18), 1),
        ),
        GroundStation(
            "NorfolkIsland", -29.033, 167.95, 0, Antenna(0, decibel_to_watt(18), 1)
        ),
    ]

    satellites = [
        Satellite("GEO1.Earth", Antenna(5, decibel_to_watt(30), 1)),
        Satellite("GEO2.Earth", Antenna(5, decibel_to_watt(30), 1)),
        Satellite("GEO3.Earth", Antenna(5, decibel_to_watt(30), 1)),
    ]

    report = load_gmat_report("data/OrbitParams.txt")
    report = q2(report, satellites, ground_stations)
    report = q3(report, satellites, ground_stations)
