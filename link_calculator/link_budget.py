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
        slant_range: float = None,
        atmospheric_loss: float = 1,
        path_loss: float = None,
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
            slant_range (float, km): slant_range between the transmit and receive antennas
            noise_temperature (float, Kelvin): the temperature of the environment

        """
        self._transmitter = transmitter
        self._receiver = receiver
        self._slant_range = slant_range
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
                    * self.receiver.gain_to_equiv_noise_temp
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

    @property
    def central_angle(self) -> float:
        if (
            self.transmitter.ground_coordinate is not None
            and self.receiver.ground_coordinate is not None
        ):
            return self.transmitter.ground_coordinate.central_angle(
                self.receiver.ground_coordinate
            )
        return None

    @staticmethod
    def distance(satellite: Satellite, ground_station: GroundStation) -> float:
        gamma = satellite.ground_coordinate.central_angle(
            ground_station.ground_coordinate
        )
        return slant_range(satellite.orbit.orbital_radius, gamma)

    @property
    def slant_range(self) -> float:
        return self._slant_range

    @property
    def path_loss(self) -> float:
        """
        Calculate the free space loss between two antennas

        Parameters
        ----------
            slant_range (float, km): slant_range between the transmit and receive antennas
            wavelength (float, m): frequency of the transmitter

        Returns
        -------
            path_loss (float, )

        """
        if self._path_loss is None:
            self._path_loss = (
                self.transmitter.transmit.wavelength
                / (4 * np.pi * self.slant_range * 1000)
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

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Carrier Power Density",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.receiver_carrier_power),
                },
                {
                    "name": "Free-Space Path Loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.path_loss),
                },
                {
                    "name": "Atmospheric Loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.atmospheric_loss),
                },
                {
                    "name": "C/No Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.carrier_to_noise_density),
                },
                {
                    "name": "Eb/No Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.eb_no),
                },
                {
                    "name": "Bandwidth to Bit Rate Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.bandwidth_to_bit_rate),
                },
                {
                    "name": "C/N Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.carrier_to_noise),
                },
                {"name": "Central Angle", "unit": "°", "value": self.central_angle},
                {"name": "Slant Range", "unit": "km", "value": self.slant_range},
            ]
        )
        receiver = self.receiver.summary()
        receiver.index = "Receiver " + receiver.index

        transmitter = self.transmitter.summary()
        transmitter.index = "Transmitter " + transmitter.index

        summary.set_index("name", inplace=True)
        summary = pd.concat([summary, transmitter, receiver])
        return summary


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

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Eb/No Ratio",
                    "unit": "dB",
                    "value": watt_to_decibel(self.eb_no),
                },
            ]
        )

        uplink = self.uplink.summary()
        uplink.rename(columns={"value": "Uplink", "unit": "Uplink unit"}, inplace=True)
        downlink = self.downlink.summary()
        downlink.rename(
            columns={"value": "Downlink", "unit": "Downlink unit"}, inplace=True
        )
        summary.set_index("name", inplace=True)
        summary.rename(columns={"value": "Overall"}, inplace=True)

        # Merge uplink and downlink summaries
        summary = pd.concat([summary, uplink, downlink], axis=1)

        # Merge unit columns
        summary["unit"] = summary["unit"].combine_first(
            summary["Uplink unit"].combine_first(summary["Downlink unit"])
        )
        summary.drop(columns=["Downlink unit", "Uplink unit"], inplace=True)

        # Clean and reformat columns
        summary = summary[
            [
                not (
                    idx.startswith("Transmitter Receive")
                    or idx.startswith("Receiver Transmit")
                )
                for idx in summary.index
            ]
        ]
        summary.rename(
            index={
                k: k.replace("Receiver Receive", "Receiver")
                if "Receiver Receive" in k
                else k
                for k in summary.index
            },
            inplace=True,
        )
        summary.rename(
            index={
                k: k.replace("Transmitter Transmit", "Transmitter")
                if "Transmitter Transmit" in k
                else k
                for k in summary.index
            },
            inplace=True,
        )
        return summary
