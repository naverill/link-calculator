from math import sqrt

from link_calculator.components.antennas import Antenna
from link_calculator.constants import EARTH_MU, EARTH_RADIUS
from link_calculator.orbits.utils import KeplerianElements


class Transmitter:
    def __init__(self, name: str, antenna: Antenna):
        self._antenna = antenna
        self._name = name


class GroundStation(Transmitter):
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
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        super().__init__(self, name, antenna)


class Satellite(Transmitter):
    def __init__(self, name: str, antenna: Antenna, orbit: KeplerianElements):
        self._orbit = orbit
        super().__init__(self, name, antenna)

    def velocity(self, orbital_radius: float, mu: float = EARTH_MU) -> float:
        """
        Calculate the velocity of a satellite in orbit according to Kepler's second law

        Parameters
        ---------
            semi_major_axis (float, km): The semi-major axis of the orbit
                orbital_radius (float, km): distance from the centre of mass to the satellite
            mu (float, optional): Kepler's gravitational constant

        Returns
        ------
            velocity (float, km/s): the orbit speed of the satellite
        """
        return sqrt(mu * (2 / orbital_radius - 1 / self.semi_major_axis))

    @property
    def semi_major_axis(self) -> float:
        return self._orbit.semi_major_axis
