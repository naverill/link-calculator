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
        ground_coordinate: GeodeticCoordinate = None,
        combined_gain: float = None,
        noise_figure: float = None,
        noise_temperature: float = None,
        gain_to_equiv_noise_temp: float = None,
        equiv_noise_temp: float = None,
    ):
        self._name = name
        self._transmit = transmit
        self._receive = receive
        self._ground_coordinate = (ground_coordinate,)
        self._noise_figure = noise_figure
        self._noise_temperature = noise_temperature
        self._combined_gain = combined_gain
        self._gain_to_equiv_noise_temp = gain_to_equiv_noise_temp
        self._equiv_noise_temp = equiv_noise_temp

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
            if self.receive.signal_to_noise is not None:
                self.noise_figure = (
                    self.receive.signal_to_noise / self.transmit.signal_to_noise
                )
            elif self.noise_temperature is not None:
                self._noise_figure = 1 + (
                    self.equiv_noise_temp / self.noise_temperature
                )
        return self._noise_figure

    @property
    def output_noise_power(self) -> float:
        return self.receive.amplifier.gain * (
            self.receive.noise_power + self.receive.amplifier.noise_power
        )

    @property
    def equiv_noise_temp(self):
        """
        TODO
        """
        if self._equiv_noise_temp is None:
            if self.noise_temperature is not None:
                self._equiv_noise_temp = self.noise_temperature * (
                    self.noise_figure - 1
                )
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
            self._combined_gain = self.receive.amplifier.gain * self.receive.gain
        return self._combined_gain

    @property
    def gain_to_equiv_noise_temp(self) -> float:
        if self._gain_to_equiv_noise_temp is None:
            if self.equiv_noise_temp is not None:
                self._equiv_noise_temp = self.combined_gain / self.equiv_noise_temp
            elif self.noise_density is not None:
                self._gain_to_equiv_noise_temp = (
                    self.carrier_power * BOLTZMANN_CONSTANT
                ) / (self.noise_density * self.receive_carrier_power)
        return self._gain_to_equiv_noise_temp

    @property
    def ground_coordinate(self) -> GeodeticCoordinate:
        return self._ground_coordinate

    @property
    def receive(self) -> Antenna:
        return self._receive

    @property
    def transmit(self) -> Antenna:
        return self._transmit

    @property
    def amplifier(self) -> Amplifier:
        return self._amplifier

    @property
    def noise_temperature(self) -> float:
        return self._noise_temperature

    @property
    def noise_density(self) -> float:
        return self._noise_density


class GroundStation(Communicator):
    def __init__(
        self,
        name: str,
        transmit: Antenna,
        receive: Antenna,
        ground_coordinate: GeodeticCoordinate = None,
        gain_to_equiv_noise_temp: float = None,
    ):
        """

        Parameters
        ----------
            name (str,): name of the ground station
            latitude (str, deg): the latitude of the groundstation
            longitude (str, deg): the longitude of the groundstation
            altitude (str, km): the altitude of the groundstation above sea level
        """
        super().__init__(
            name=name,
            transmit=transmit,
            receive=receive,
            ground_coordinate=ground_coordinate,
            gain_to_equiv_noise_temp=gain_to_equiv_noise_temp,
        )


class Satellite(Communicator):
    def __init__(
        self,
        name: str,
        transmit: Antenna,
        receive: Antenna,
        orbit: KeplerianElements = None,
        ground_coordinate: GeodeticCoordinate = None,
        gain_to_equiv_noise_temp: float = None,
        combined_gain: float = None,
    ):
        self._orbit = orbit
        super().__init__(
            name=name,
            transmit=transmit,
            receive=receive,
            ground_coordinate=ground_coordinate,
            combined_gain=combined_gain,
            gain_to_equiv_noise_temp=gain_to_equiv_noise_temp,
        )

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
