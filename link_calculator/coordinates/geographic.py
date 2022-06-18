from math import acos, atan, cos, degrees, pi, radians, sin, sqrt, tan

import pandas as pd


class GeodeticCoordinate:
    def __init__(self, latitude: float, longitude: float, altitude: float = 0):
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def altitude(self) -> float:
        return self._altitude

    def central_angle(
        self,
        point: "GeodeticCoordinate",
    ) -> float:
        """
        Calculate angle gamma at the centre of the ground, between the Earth station and the satellite

        Parameters
        ---------
            ground_station_lat (float, deg): the latitude of the ground station
            ground_station_long (float, deg): the longitude of the ground station
            sat_lat (float, deg): the latitude of the satellite
            sat_long (float, deg): the longitude of the satellite

        Returns
        ------
            gamma (float, rad): angle between satellite and ground station
        """
        gamma = acos(
            cos(radians(self.latitude))
            * cos(radians(point.latitude))
            * cos(radians(point.longitude) - radians(self.longitude))
            + sin(radians(self.latitude)) * sin(radians(point.latitude))
        )
        return degrees(gamma)

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {"name": "Latitude", "unit": "°", "value": self.latitude},
                {"name": "Longitude", "unit": "°", "value": self.longitude},
                {"name": "Altitude", "unit": "°", "value": self.altitude},
            ]
        )
        summary.set_index("name", inplace=True)
        return summary
