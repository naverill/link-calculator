from link_calculator.components.antennas import Antenna


class GroundStation:
    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
        antenna: Antenna,
    ):
        """

        Parameters
        ----------
            name (str,): name of the ground station
            latitude (str, deg): the latitude of the groundstation
            longitude (str, deg): the longitude of the groundstation
            altitude (str, km): the altitude of the groundstation above sea level
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.antenna = antenna
