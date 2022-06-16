from math import sqrt

import pandas as pd

from link_calculator.components.antennas import Amplifier, Antenna
from link_calculator.constants import BOLTZMANN_CONSTANT, EARTH_MU, EARTH_RADIUS
from link_calculator.conversions import GHz_to_Hz, watt_to_decibel
from link_calculator.orbits.utils import GeodeticCoordinate, Orbit


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
        noise_density: float = None,
        gain_to_equiv_noise_temp: float = None,
        equiv_noise_temp: float = None,
    ):
        self._name = name
        self._transmit = transmit
        self._receive = receive
        self._ground_coordinate = ground_coordinate
        self._noise_figure = noise_figure
        self._noise_density = noise_density
        self._noise_temperature = noise_temperature
        self._combined_gain = combined_gain
        self._gain_to_equiv_noise_temp = gain_to_equiv_noise_temp
        self._equiv_noise_temp = equiv_noise_temp
        self.propagate_calculations()

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
            if self._isset(self.receive.signal_to_noise):
                self.noise_figure = (
                    self.receive.signal_to_noise / self.transmit.signal_to_noise
                )
            elif self._isset(self._noise_temperature):
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
    def receive_noise_power(self) -> float:
        return (
            BOLTZMANN_CONSTANT
            * self.noise_temperature
            * GHz_to_Hz(self.receive.modulation.bandwidth)
        )

    @property
    def equiv_noise_temp(self):
        """
        TODO
        """
        if self._equiv_noise_temp is None:
            if self._isset(self._noise_temperature):
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
            if self._isset(self.receive.amplifier):
                self._combined_gain = self.receive.amplifier.gain * self.receive.gain
            else:
                self._combined_gain = self.receive.gain
        return self._combined_gain

    @property
    def gain_to_equiv_noise_temp(self) -> float:
        if self._gain_to_equiv_noise_temp is None:
            if self._isset(self._equiv_noise_temp):
                self._gain_to_equiv_noise_temp = (
                    self.combined_gain / self.equiv_noise_temp
                )
            elif self._isset(self._noise_density):
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
    def noise_temperature(self) -> float:
        return self._noise_temperature

    @property
    def noise_density(self) -> float:
        return self._noise_density

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {"name": "Noise Figure", "unit": "", "value": self.noise_figure},
                {
                    "name": "Equivalent Noise Temperature",
                    "unit": "K",
                    "value": self.equiv_noise_temp,
                },
                {
                    "name": "Noise Temperature",
                    "unit": "K",
                    "value": self.noise_temperature,
                },
                {
                    "name": "Combined Gain",
                    "unit": "dB",
                    "value": watt_to_decibel(self.combined_gain),
                },
                {
                    "name": "G/Te Ratio",
                    "unit": "dBK-1",
                    "value": watt_to_decibel(self.gain_to_equiv_noise_temp),
                },
            ]
        )
        transmitter = self.transmit.summary()
        transmitter.index = "Transmit " + transmitter.index

        receiver = self.receive.summary()
        receiver.index = "Receive " + receiver.index

        summary.set_index("name", inplace=True)
        summary = pd.concat([summary, transmitter, receiver])
        return summary

    def propagate_calculations(self) -> float:
        for _ in range(3):
            for var in type(self).__dict__:
                getattr(self, var)

    def _isset(self, *args) -> bool:
        return not (None in args)


class GroundStation(Communicator):
    def __init__(
        self,
        name: str,
        transmit: Antenna,
        receive: Antenna,
        ground_coordinate: GeodeticCoordinate = None,
        gain_to_equiv_noise_temp: float = None,
        combined_gain: float = None,
        noise_figure: float = None,
        noise_temperature: float = None,
        equiv_noise_temp: float = None,
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
            noise_figure=noise_figure,
            noise_temperature=noise_temperature,
            equiv_noise_temp=equiv_noise_temp,
        )

    def summary(self) -> pd.DataFrame:
        summary = super().summary()
        if self.ground_coordinate is not None:
            coordinate = self.ground_coordinate.summary()
            coordinate.index = "Earth Station " + coordinate.index
            summary = pd.concat([summary, coordinate])
        return summary


class Satellite(Communicator):
    def __init__(
        self,
        name: str,
        transmit: Antenna,
        receive: Antenna,
        orbit: Orbit = None,
        ground_coordinate: GeodeticCoordinate = None,
        gain_to_equiv_noise_temp: float = None,
        combined_gain: float = None,
        noise_figure: float = None,
        noise_temperature: float = None,
        equiv_noise_temp: float = None,
    ):
        self._orbit = orbit
        super().__init__(
            name=name,
            transmit=transmit,
            receive=receive,
            ground_coordinate=ground_coordinate,
            combined_gain=combined_gain,
            gain_to_equiv_noise_temp=gain_to_equiv_noise_temp,
            noise_figure=noise_figure,
            noise_temperature=noise_temperature,
            equiv_noise_temp=equiv_noise_temp,
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
        if self.orbit is not None:
            return self.orbit.semi_major_axis
        return None

    @property
    def orbit(self) -> float:
        return self._orbit

    def summary(self) -> pd.DataFrame:
        summary = super().summary()
        if self._isset(self.ground_coordinate):
            coordinate = self.ground_coordinate.summary()
            coordinate.index = "Sub-Satellite " + coordinate.index
            summary = pd.concat([summary, coordinate])
        return summary
