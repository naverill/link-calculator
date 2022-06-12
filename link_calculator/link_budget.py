import numpy as np
import pandas as pd

from link_calculator.components.communicators import (
    Communicator,
    GroundStation,
    Satellite,
)
from link_calculator.constants import BOLTZMANN_CONSTANT
from link_calculator.orbits.utils import slant_range
from link_calculator.propagation.conversions import watt_to_decibel
from link_calculator.signal_processing.conversions import GHz_to_Hz


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
        receiver_carrier_power: float = None,
        noise_temperature: float = None,
        carrier_to_noise_density: float = None,
        carrier_to_noise: float = None,
        bandwidth_to_bit_rate: float = None,
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
        self._receiver_carrier_power = receiver_carrier_power
        self._noise_temperature = noise_temperature
        self._carrier_to_noise_density = carrier_to_noise_density
        self._carrier_to_noise = carrier_to_noise
        self._bandwidth_to_bit_rate = bandwidth_to_bit_rate
        self._eb_no = eb_no

    @property
    def carrier_to_noise_density(self) -> float:
        if self._carrier_to_noise_density is None:
            if self.receiver.equiv_noise_temp is not None:
                self._carrier_to_noise_density = (
                    self.receiver.combined_gain * self.receiver_carrier_power
                ) / (BOLTZMANN_CONSTANT * self.receiver.equiv_noise_temp)
            elif self.receiver.gain_to_equiv_noise_temp is not None:
                self._carrier_to_noise_density = (
                    self.transmitter.transmit.eirp
                    * self.path_loss
                    * self.atmospheric_loss
                    * self.receiver.receive.loss
                    * self.transmitter.gain_to_equiv_noise_temp
                    / BOLTZMANN_CONSTANT
                )
        return self._carrier_to_noise_density

    @property
    def eb_no(self) -> float:
        if self._eb_no is None:
            if self.carrier_to_noise_density is not None:
                self._eb_no = (
                    self.carrier_to_noise_density
                    / self.transmitter.transmit.modulation.bit_rate
                )
            elif self.carrier_to_noise is not None:
                self._eb_no = (
                    self.carrier_to_noise
                    * GHz_to_Hz(self.transmitter.transmit.modulation.bandwidth)
                    * self.transmitter.transmit.modulation.bit_rate
                )
        return self._eb_no

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_to_noise is None:
            self._carrier_to_noise = self.eb_no / self.bandwidth_to_bit_rate
        return self._carrier_to_noise

    @property
    def bandwidth_to_bit_rate(self) -> float:
        if self._bandwidth_to_bit_rate is None:
            self._bandwidth_to_bit_rate = (
                GHz_to_Hz(self.transmitter.transmit.modulation.bandwidth)
                / self.transmitter.transmit.modulation.bit_rate
            )
        return self._bandwidth_to_bit_rate

    @property
    def receiver_carrier_power(self) -> float:
        if self._receiver_carrier_power is None:
            self._receiver_carrier_power = (
                self.transmitter.transmit.eirp * self.path_loss * self.atmospheric_loss
            )
        return self._receiver_carrier_power

    @staticmethod
    def distance(satellite: Satellite, ground_station: GroundStation) -> float:
        gamma = ground_station.ground_coordinate.central_angle(
            satellite.ground_coordinate
        )
        return slant_range(satellite.orbit.orbital_radius, gamma)

    @property
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
            self._noise_power = self.noise_density * GHz_to_Hz(
                self.transmitter.transmit.modulation.bandwidth
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
                / GHz_to_Hz(self.transmitter.transmit.modulation.bandwidth)
            ) / BOLTZMANN_CONSTANT
        return self._noise_temperature

    @property
    def receiver(self) -> Communicator:
        return self._receiver

    @property
    def transmitter(self) -> Communicator:
        return self._transmitter

    @property
    def atmospheric_loss(self) -> float:
        return self._atmospheric_loss

    def get_link_table(self) -> pd.DataFrame:
        link_table = pd.DataFrame.from_records(
            [
                {
                    "name": "Transmitter amplifier output P at saturation",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.transmitter.transmit.amplifier.power),
                },
                {
                    "name": "Transmitter back-off loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.transmitter.transmit.amplifier.loss),
                },
                {
                    "name": "Transmitter feeder loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.transmitter.transmit.loss),
                },
                {
                    "name": "Transmitter antenna gain",
                    "unit": "dB",
                    "value": watt_to_decibel(self.transmitter.transmit.gain),
                },
                {
                    "name": "Transmitter EIRP",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.transmitter.transmit.eirp),
                },
                {
                    "name": "Free-space path loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.path_loss),
                },
                {
                    "name": "Atmospheric loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.atmospheric_loss),
                },
                {
                    "name": "Carrier power density at receiver",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.receiver_carrier_power),
                },
                {
                    "name": "Receiver feeder loss",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.receiver.receive.loss),
                },
                {
                    "name": "Gain to equivalent noise temperature ratio",
                    "unit": "dBK-1",
                    "value": watt_to_decibel(self.transmitter.gain_to_equiv_noise_temp),
                },
                {
                    "name": "Boltzmann's constant",
                    "unit": "dB",
                    "value": watt_to_decibel(BOLTZMANN_CONSTANT),
                },
                {
                    "name": "Carrier to noise density ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.carrier_to_noise_density),
                },
                {
                    "name": "Bit rate",
                    "unit": "dB",
                    "value": watt_to_decibel(
                        self.transmitter.transmit.modulation.bit_rate
                    ),
                },
                {
                    "name": "Eb/No ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.eb_no),
                },
                {
                    "name": "Bandwidth to bit rate ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.bandwidth_to_bit_rate),
                },
                {
                    "name": "Carrier to noise ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.carrier_to_noise),
                },
            ]
        )
        link_table.set_index("name", inplace=True)
        return link_table


class LinkBudget:
    def __init__(
        self,
        uplink: Link,
        downlink: Link,
    ):
        self._uplink = uplink
        self._downlink = downlink

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

    def get_link_budget(self) -> pd.DataFrame:
        uplink = self.uplink.get_link_table()
        uplink.index = "Uplink " + uplink.index
        downlink = self.downlink.get_link_table()
        downlink.index = "Downlink " + downlink.index
        link_budget = pd.concat([uplink, downlink])
        link_budget.loc["Overall EbNo"] = ["dB", watt_to_decibel(self.eb_no)]
        return link_budget
