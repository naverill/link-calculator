import numpy as np
from link_calulator.orbits.utils import slant_range

from link_calculator.components.communicators import (
    Communicator,
    GroundStation,
    Satellite,
)
from link_calculator.constants import BOLTZMANN_CONSTANT


class Link:
    def __init__(
        self,
        transmitter: Communicator,
        receiver: Communicator,
        distance: float = None,
        atmospheric_loss: float = 1,
        path_loss: float = 1,
        min_elevation: float = 0,
        transmitter_eirp: float = None,
        receive_carrier_power: float = None,
        noise_temperature: float = None,
        carrier_to_noise_density: float = None,
        carrier_to_noise: float = None,
        eb_no: float = None,
    ):
        """


        Parameters
        ----------
            distance (float, km): distance between the transmit and receive antennas
            noise_temperature (float, Kelvin): the temperature of the environment

        """
        self._transmitter = transmitter
        self._receiver = receiver
        self._distance = distance
        self._atmospheric_loss = atmospheric_loss
        self._path_loss = path_loss
        self._min_elevation = min_elevation
        self._transmitter_eirp = transmitter_eirp
        self._receive_carrier_power = receive_carrier_power
        self._noise_temperature = noise_temperature
        self._carrier_to_noise_density = carrier_to_noise_density
        self._carrier_to_noise = carrier_to_noise
        self._eb_no = eb_no

    @property
    def carrier_to_noise_density(self) -> float:
        if self._carrier_to_noise_density is None:
            self._carrier_to_noise_density = (
                self.receiver.combined_gain * self.receiver_carrier_power
            ) / (BOLTZMANN_CONSTANT * self.receiver.equiv_noise_temp)
        return self._carrier_to_noise_density

    @property
    def eb_no(self) -> float:
        if self._eb_no is None:
            if self.carrier_to_noise_density is not None:
                self._eb_no = (
                    self.carrier_to_noise_density
                    / self.transmitter.transmit.modulation.bit_period
                )
            else:
                self._eb_no = (
                    self.carrier_to_noise
                    * self.transmitter.transmit.modulation.bandwidth
                    * self.transmitter.transmit.modulation.bit_rate
                )
        return self._eb_no

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_to_noise is None:
            self._carrier_to_noise = self.eb_no / (
                self.transmitter.transmit.modulation.bandwidth
                * self.transmitter.transmit.modulation.bit_rate
            )
        return self._carrier_to_noise

    @property
    def transmitter_eirp(self) -> float:
        if self._transmitter_eirp is None:
            self._transmitter_eirp = (
                self.transmitter.amplifier.power
                * self.transmitter.amplifier.loss
                * self.transmitter.antenna.loss
                * self.transmitter.antenna.gain
            )
        return self._transmitter_eirp

    @property
    def receiver_carrier_power(self) -> float:
        if self._receiver_carrier_power is None:
            self._receiver_carrier_power = (
                self.transmitter_eirp * self.path_loss * self.atmospheric_loss
            )
        return self._receiver_carrier_power

    @staticmethod
    def distance(self, satellite: Satellite, ground_station: GroundStation) -> float:
        gamma = ground_station.ground_coordinate.central_angle(
            satellite.ground_coordinate
        )
        return slant_range(satellite.orbit.orbital_radius, gamma)

    @distance.setter
    def distance(self, value) -> None:
        self._distance = value

    def path_loss(self) -> float:
        """
        Calculate the free space loss between two antennas

        Parameters
        ----------
            distance (float, km): distance between the transmit and receive antennas
            wavelength (float, m): frequency of the transmitter

        Returns
        -------
            path_loss (float, )

        """
        if self._path_loss is None:
            self._path_loss = (
                self.transmitter.transmit.wavelength
                / (4 * np.pi * self.distance * 1000)
            ) ** 2
        return self._path_loss

    @property
    def noise_power(self) -> float:
        """
        Returns
        ----------
            noise_power (float, ): sum of the input noise power and the noise power
                added by the amplifier
        """
        if self._noise_power is None:
            self._noise_power = (
                self.noise_density
                * self.transmitter.transmit.modulation.bandwidth
                * 1e9
            )
        return self._noise_power

    @property
    def noise_density(self) -> float:
        """
        Calculate the noise density of the system

        Returns
        -------
            noise_density (float, W/Hz): the total noise power, normalised to a 1-Hz bandwidth
        """
        if self._noise_density is None:
            self._noise_density = BOLTZMANN_CONSTANT * self.noise_temperature
        return self.noise_density

    @property
    def noise_temperature(self) -> float:
        """

        Returns
        -------
            noise_temperature (float, K): ambient temperature of the environment
        """
        if self._noise_temperature is None:
            self._noise_temperature = (
                self.noise_power
                / (self.transmitter.transmit.modulation.bandwidth * 1e9)
            ) / BOLTZMANN_CONSTANT
        return self._noise_temperature


class LinkBudget:
    def __init__(
        self,
        uplink: Link,
        downlink: Link,
    ):
        self._uplink = uplink
        self._downlink = downlink

    @property
    def ground_station_carrier_power(self, distance) -> float:
        return self.downlink.receiver_carrier_power

    @property
    def satellite_carrier_power(self, distance) -> float:
        return self.uplink.receiver_carrier_power

    @property
    def eb_no(self) -> float:
        return (self.uplink.eb_no * self.downlink.eb_no) / (
            self.uplink.eb_no + self._downlink.eb_no
        )

    @property
    def uplink(self) -> Link:
        return self._uplink

    @property
    def downlink(self) -> Link:
        return self._downlink
