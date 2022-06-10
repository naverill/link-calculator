from math import sqrt

from link_calculator.components.antennas import Amplifier, Antenna
from link_calculator.constants import BOLTZMANN_CONSTANT, EARTH_MU, EARTH_RADIUS
from link_calculator.orbits.utils import GeodeticCoordinate, KeplerianElements


class Communicator:
    def __init__(
        self,
        name: str,
        transmit: Antenna,
        receive: Antenna,
        amplifier: Amplifier = None,
        combined_gain: float = None,
        noise_figure: float = None,
        noise_temperature: float = None,
    ):
        self._name = name
        self._transmit = transmit
        self._receive = receive
        self._noise_figure = noise_figure
        self._noise_temperature = noise_temperature
        self._combined_gain = combined_gain

    @property
    def noise_figure(self) -> float:
        """
        Calculate the noise figure of the device

        Returns
        -------
            noise_figure (float, ):  the ratio of the S/N ratio at the input to the
                S/N ratio at the output. Measure of the relative increase in noise
                power compared to increase in signal power
        """
        if self._noise_figure is None:
            self.noise_figure = (
                self.receive.signal_to_noise / self.transmit.signal_to_noise
            )

            self._noise_figure = 1 + (self.equiv_noise_temp / self.noise_temperature)
        return self._noise_figure

    @property
    def receive_carrier_to_noise(self) -> float:
        if self._receive_carrier_to_noise is None:
            self._receive_carrier_to_noise = (
                self.receive.carrier_power * self.combined_gain
            ) / (BOLTZMANN_CONSTANT * self.equiv_noise_temp)
        return self._receive_carrier_to_noise

    @property
    def output_noise_power(self) -> float:
        return self.amplifier.gain * (
            self.receive.noise_power + self.amplifier.noise_power
        )

    @property
    def equiv_noise_temp(self):
        """
        TODO
        """
        if self._equiv_noise_temp is None:
            self._equiv_noise_temp = self.noise_temperature * (self.noise_figure - 1)
        return self._equiv_noise_temp

    @equiv_noise_temp.setter
    def equiv_noise_temp(self, value):
        """
        TODO
        """
        self._equiv_noise_temp = value

    @property
    def combined_gain(self) -> float:
        if self._combined_gain is None:
            self._combined_gain = self.amplifier.gain * self.receive.gain
        return self._combined_gain

    @property
    def gain_to_noise_temp(self) -> float:
        if self._gain_to_noise_temp is None:
            self._gain_to_noise_temp = (self.carrier_power * BOLTZMANN_CONSTANT) / (
                self.noise_density * self.receive_carrier_power
            )
        return self._gain_to_noise_ratio


class GroundStation(Communicator):
    def __init__(
        self,
        name: str,
        coordinate: GeodeticCoordinate,
        transmit: Antenna,
        receive: Antenna,
        amplifier: Amplifier,
    ):
        """

        Parameters
        ----------
            name (str,): name of the ground station
            latitude (str, deg): the latitude of the groundstation
            longitude (str, deg): the longitude of the groundstation
            altitude (str, km): the altitude of the groundstation above sea level
        """
        self.coordinate = coordinate
        super().__init__(self, name, transmit, receive, amplifier)


class Satellite(Communicator):
    def __init__(
        self,
        name: str,
        transmit: Antenna,
        receive: Antenna,
        amplifier: Amplifier,
        orbit: KeplerianElements,
        sub_satellite_point: GeodeticCoordinate,
        combined_gain: float = None,
    ):
        self._orbit = orbit
        self._sub_sat_point = sub_satellite_point
        super().__init__(self, name, transmit, receive, amplifier, combined_gain)

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

    @property
    def sub_satellite_point(self) -> GeodeticCoordinate:
        return self._sub_satellite_point
