import numpy as np
import pandas as pd
import plotly.express as px

from link_calculator.components import Antenna, GroundStation, Satellite
from link_calculator.orbits.utils import (
    angle_sat_to_ground_station,
    elevation_angle,
    slant_range,
)
from link_calculator.propagation.conversions import (
    decibel_to_watt,
    frequency_to_wavelength,
    watt_to_decibel,
)
from link_calculator.propagation.utils import receive_power


def load_gmat_report(file_path):
    return pd.read_csv(file_path, sep="\s{2,}", engine="python")


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

    plot_elevation(report, satellites, ground_stations)
    return report


def q3(
    report: pd.DataFrame,
    satellites: list[str],
    ground_stations: list[GroundStation],
):
    for gs in ground_stations:
        for sat in satellites:
            report[f"{sat.name}.Earth.ReceivePower.{gs.name}"] = report.apply(
                lambda row: watt_to_decibel(
                    receive_power(
                        sat.antenna.power,
                        sat.antenna.loss,
                        sat.antenna.gain,
                        row[f"{sat.name}.Earth.SlantRange.{gs.name}"] * 1000,
                        gs.antenna.loss,
                        gs.antenna.gain,
                        1,
                        wavelength=frequency_to_wavelength(sat.antenna.frequency),
                    )
                )
                if row[f"{sat.name}.Earth.Elevation.{gs.name}"] > 20
                else None,
                axis=1,
            )
    plot_receive_power(report, satellites, ground_stations)
    return report


def plot_receive_power(report, satellites, ground_stations):
    for gs in ground_stations:
        min_slant = report.iloc[
            report[f"{satellites[0].name}.Earth.SlantRange.{gs.name}"].idxmin()
        ]

        fig = px.line(
            report,
            x="UTC Gregorian",
            y=[f"{sat.name}.Earth.ReceivePower.{gs.name}" for sat in satellites],
            labels={"value": "Receive Power (dBW)"},
        )
        fig.add_vline(x=min_slant["UTC Gregorian"], line_dash="dash")
        fig.add_annotation(
            x=min_slant["UTC Gregorian"],
            y=min_slant[f"{satellites[0].name}.Earth.ReceivePower.{gs.name}"],
            text=f"Slant range = {min_slant[f'{satellites[0].name}.Earth.SlantRange.{gs.name}']:.2f}",
        )
        fig.update_layout(
            title={
                "text": f"Power received by {gs.name}",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            }
        )
        fig.show()
        print(
            gs.name,
            min_slant[f"{satellites[0].name}.Earth.ReceivePower.{gs.name}"],
            "dBW",
        )


def plot_elevation(report, satellites, ground_stations):
    for gs in ground_stations:
        min_slant = report.iloc[
            report[f"{satellites[0].name}.Earth.SlantRange.{gs.name}"].idxmin()
        ]

        cols = [f"{sat.name}.Earth.Elevation.{gs.name}" for sat in satellites]
        elevation = report[cols]
        elevation = elevation[elevation > 20]
        elevation["UTC Gregorian"] = report["UTC Gregorian"]

        fig = px.line(
            elevation,
            x="UTC Gregorian",
            y=cols,
            labels={"value": "Elevation (deg)"},
        )
        fig.add_vline(x=min_slant["UTC Gregorian"], line_dash="dash")
        fig.add_annotation(
            x=min_slant["UTC Gregorian"],
            y=min_slant[f"{satellites[0].name}.Earth.Elevation.{gs.name}"],
            text=f"Slant range = {min_slant[f'{satellites[0].name}.Earth.SlantRange.{gs.name}']:.2f}",
        )
        fig.update_layout(
            title={
                "text": f"Elevation above {gs.name}",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            }
        )
        fig.show()
        print(gs.name, min_slant[f"{satellites[0].name}.Earth.Altitude"], "km")


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
        GroundStation(
            "MacquarieResearchStation",
            -54.5,
            158.95,
            0,
            Antenna("MacquarieReceive", 0, decibel_to_watt(18), 1, gs_frequency),
        ),
    ]

    satellites = [
        Satellite(
            "COMMSAT1",
            Antenna("COMMSAT1Transmit", 5, decibel_to_watt(30), 1, sat_frequency),
        ),
        Satellite(
            "COMMSAT2",
            Antenna("COMMSAT2Transmit", 5, decibel_to_watt(30), 1, sat_frequency),
        ),
        Satellite(
            "COMMSAT3",
            Antenna("COMMSAT3Transmit", 5, decibel_to_watt(30), 1, sat_frequency),
        ),
    ]

    report = load_gmat_report("input/OrbitParams.txt")
    report["UTC Gregorian"] = pd.to_datetime(report["COMMSAT1.UTCGregorian"])
    report = q2(report, satellites, ground_stations)
    report = q3(report, satellites, ground_stations)
    report.to_csv("output/report.csv")
