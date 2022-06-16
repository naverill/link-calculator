from math import cos, degrees, exp, pi, radians, sin

import numpy as np
import pandas as pd

from link_calculator.constants import BOLTZMANN_CONSTANT
from link_calculator.conversions import (
    frequency_to_wavelength,
    watt_to_decibel,
    wavelength_to_frequency,
)
from link_calculator.signal_processing.modulation import Modulation


class Amplifier:
    def __init__(
        self, power: float, gain: float = 1, loss: float = 1, noise_power: float = None
    ):
        """
        Parameters
        ----------
            loss (float, ): losses in the amplifier (e.g. back-off loss)
            power (float, W): the total output amplifier power
        """
        self._power = power
        self._gain = gain
        self._loss = loss
        self._noise_power = noise_power

    @property
    def power(self) -> float:
        """
        TODO
        Returns
        -------
            power (float, W): the total output amplifier power
        """
        return self._power

    @property
    def gain(self) -> float:
        """
        TODO
        Returns
        -------
        """
        return self._gain

    @property
    def loss(self) -> float:
        """
        TODO
        Returns
        -------
        """
        return self._loss

    @property
    def noise_power(self) -> float:
        """
        TODO
        Returns
        -------
        """
        return self._noise_power

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Power",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.power),
                },
                {
                    "name": "Gain",
                    "unit": "dB",
                    "value": watt_to_decibel(self.gain),
                },
                {
                    "name": "Back-Off Loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.loss),
                },
                {
                    "name": "Noise Power",
                    "unit": "dB",
                    "value": watt_to_decibel(self.noise_power),
                },
            ]
        )
        summary.set_index("name", inplace=True)
        return summary


class Antenna:
    def __init__(
        self,
        gain: float = None,
        loss: float = 1,
        eirp: float = None,
        frequency: float = None,
        wavelength: float = None,
        effective_aperture: float = None,
        cross_sect_area: float = None,
        cross_sect_diameter: float = None,
        half_beamwidth: float = None,
        efficiency: float = None,
        roughness_factor: float = None,
        carrier_to_noise: float = None,
        signal_to_noise: float = None,
        carrier_power: float = None,
        modulation: Modulation = None,
        combined_loss: float = None,
        amplifier: Amplifier = None,
        gain_to_noise_temperature=None,
        power_density: float = None,
    ):
        """
        Instantiate an Antenna object

        Parameters
        ----------
            name (str): Name of antenna
            gain (float, ): ratio of maximum power densiry to that of an isotropic radiatior
                at the same distance in the direction of the receiving antenna
            loss (float, ): coupling loss between transmitter and antenna
                in the range [0, 1]
            frequency (float, GHz): the transmit frequency of the antenna
            wavelength (float, m): the radiation wavelength
            cross_sect_area (float, m^2): cross sectional area of the antenna aperture
            cross_sect_diameter (float, m): cross sectional diameter of the antenna aperture
            effective_aperture (float, m^2): The effective collecting area of a receiving antenna
            half_beamwidth (float, deg): The angle between the directions providing half maximum power
                on either side of the maximum power direction.
            efficiency (float, ): the efficiency with which the antenna radiates all
              energy fed into it
            roughness_factor (float, m): rms roughness of the antenna dish surface
        """
        self._amplifier = amplifier
        self._gain = gain
        self._loss = loss
        self._eirp = eirp
        self._efficiency = efficiency
        self._half_beamwidth = half_beamwidth
        self._cross_sect_area = cross_sect_area
        self._cross_sect_diameter = cross_sect_diameter
        self._frequency = frequency
        self._wavelength = wavelength
        self._modulation = modulation
        self._effective_aperture = effective_aperture
        self._roughness_factor = roughness_factor
        self._carrier_to_noise = carrier_to_noise
        self._signal_to_noise = signal_to_noise
        self._carrier_power = carrier_power
        self._gain_to_noise_temperature = gain_to_noise_temperature
        self._combined_loss = combined_loss
        self._power_density = power_density

    def power_density_eirp(self, distance: float, atmospheric_loss: float = 1) -> float:
        """
        Calculate the power density of the wavefront using EIRP

        Parameters
        ---------
            eirp (float, dB)
            distance (float, km): the distance between the transmit and receive antennas
            atmospheric_loss (float, ): the total losses due to the atmosphere

        Returns
        ------
            power_density (float, W/m^2): the power density at distance d
        """
        distance = distance * 1000  # convert to m
        return self.eirp / (4 * np.pi * distance**2) * atmospheric_loss

    def power_density_distance(self, distance: float) -> float:
        """
        Calculate the power density of the wavefront

        Parameters
        ---------
            power (float, W): the transmitted power
            distance (float, km): the distance between the transmit and receive antennas

        Returns
        ------
            power_density (float, W/m^2): the power density at distance d
        """
        distance = distance * 1000  # convert to m
        return (self.amplifier.power * self.gain) / (4 * np.pi * distance**2)

    @property
    def combined_loss(self) -> float:
        if self._combined_loss is None:
            if self._isset(self.amplifier):
                self._combined_loss = self.loss * self.amplifier.loss
            elif self._isset(self._eirp):
                self._combined_loss = self.eirp / (self.amplifier.power * self.gain)
        return self._combined_loss

    @property
    def eirp(self) -> float:
        """
        Calculate the Effetive Isotropic Radiated Power


        Returns
        -------
            eirp (float, dB): power incident at the receiver that would have had to be radiated
                from an isotropic antenna to achieve the same power incident at the
                receiver  as that of a transmitter with a specific antenna gain
        """
        if self._eirp is None:
            self._eirp = self.amplifier.power * self.combined_loss * self.gain
        return self._eirp

    @property
    def half_beamwidth(self) -> float:
        if self._half_beamwidth is None:
            self._half_beamwidth = self.wavelength / (
                self.cross_sect_diameter * np.sqrt(self.efficiency)
            )
        return self._half_beamwidth

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_to_noise is None:
            self._carrier_to_noise = self.carrier_power / self.noise_density
        return self._carrier_to_noise

    @property
    def effective_aperture(self) -> float:
        """
        Calculate the effective area of the receiving antenna

        Parameters
        ----------

        Returns
        -------
            effective_aperture (float, m^2): the effective aperture of the receive antenna
        """
        if self._effective_aperture is None:
            self._effective_aperture = self.gain * self.wavelength**2 / (4 * np.pi)
        return self._effective_aperture

    @property
    def directive_gain(self) -> float:
        return self.gain / self.efficiency

    @property
    def directivity(self) -> float:
        """
        TODO
        """
        return 4 * pi * self.cross_sect_area / self.wavelength**2

    def pointing_loss(self, pointing_error: float) -> float:
        """
        TODO
        Parameters
        ---------
          pointing_error (float, deg): angle off nominal pointing direction

        Returns
        ------
          pointing_loss (float, ??):
        """
        return exp(
            -2.76 * (radians(pointing_error) / radians(self.half_beamwidth)) ** 2
        )

    def surface_roughness_loss(self) -> float:
        """
        TODO
        Parameters
        ---------

        Returns
        ------
          pointing_loss (float, ??):
        """
        if self._surface_roughness_loss is None:
            self._surface_roughness_loss = exp(
                -(4 * pi * self.roughness_factor / self.wavelength)
            )
        return self._surface_roughness_loss

    @property
    def gain(self):
        """
        TODO
        Returns
        -------
            gain (float, ): ratio of maximum power densiry to that of an isotropic radiatior
                at the same distance in the direction of the receiving antenna
        """
        if self._gain is None:
            if self._isset(self._eirp):
                self._gain = self.eirp / (self.amplifier.power * self.combined_loss)
            elif self._isset(self._efficiency):
                self._gain = (
                    self.efficiency
                    * 4
                    * np.pi
                    * self.cross_sect_area
                    / self.wavelength**2
                )
        return self._gain

    @property
    def carrier_power(self) -> float:
        return self._carrier_power

    @property
    def power_density(self) -> float:
        return self._power_density

    @power_density.setter
    def power_density(self, value):
        self._power_density = value

    @property
    def frequency(self):
        """
        TODO
        Returns
        -------
            frequency (float, GHz): the transmit frequency of the antenna
        """
        if self._frequency is None:
            self._frequency = wavelength_to_frequency(self._wavelength)
        return self._frequency

    @property
    def wavelength(self):
        """
        TODO
        """
        if self._wavelength is None:
            self._wavelength = frequency_to_wavelength(self._frequency)
        return self._wavelength

    @property
    def efficiency(self):
        """
        TODO
        """
        if self._efficiency is None:
            if self._isset(self._gain, self._cross_sect_area):
                self._efficiency = self.gain / (
                    4 * np.pi * self.cross_sect_area / self.wavelength**2
                )
        return self._efficiency

    @property
    def cross_sect_diameter(self):
        """
        TODO
        """
        return self._cross_sect_diameter

    @property
    def cross_sect_area(self):
        """
        TODO
        """
        return self._cross_sect_area

    @property
    def loss(self):
        """
        TODO
        Returns
        -------
            loss (float, ): coupling loss between transmitter and antenna
                in the range [0, 1]
        """
        if self._loss is None:
            if self._isset(self._combined_loss):
                if self._isset(self.amplifier):
                    self._loss = self.combined_loss / self.amplifier.loss
                else:
                    self._loss = self.combined_loss
        return self._loss

    @property
    def amplifier(self):
        """
        TODO
        """
        return self._amplifier

    @property
    def modulation(self):
        """
        TODO
        """
        return self._modulation

    @property
    def transmit_loss(self):
        """
        TODO
        Returns
        -------
            transmit_loss (float, ): the feeder and branching losses from the amplifier
                to the transmit antenna
        """
        return self._transmit_loss

    def receive_power(
        self,
        transmit_antenna: "Antenna",
        distance: float,
        atmospheric_loss: float = 1,
    ) -> float:
        """
        Calculate the power collected by the receive antenna

        Parameters
        ----------
            distance (float, km): the distance between the transmit and receive antennas
            atmospheric_loss (float, ): The loss due to the atmosphere

        Returns
        -------
            receive_power (float, W): the total collected power at the receiver's terminals
        """
        pow_density = transmit_antenna.power_density_eirp(distance, atmospheric_loss)
        return pow_density * self.effective_aperture * self.loss

    @property
    def roughness_factor(self):
        """
        TODO
        """
        return self._roughness_factor

    @property
    def signal_to_noise(self):
        """
        calculate S/N knowing G/T, wavelength, bandwidth and the field
        strength of the signal (Duffy 2007).

        Signal/Noise=S(λ**2/4π)(G/T)(1/kbB) where:

        S is power flux density;
        λ is wavelength;
        kb is Boltzmann’s constant; and
        B is receiver quivalent noise bandwidth
        """
        if self._signal_to_noise is None:
            if self._isset(self._gain_to_noise_temperature, self._power_density):
                self._signal_to_noise = (
                    self.power_density
                    * (self.wavelength**2 / (4 * pi))
                    * self.gain_to_noise_temperature
                    * (1 / (BOLTZMANN_CONSTANT * self.modulation.bandwidth))
                )
        return self._signal_to_noise

    @property
    def gain_to_noise_temperature(self):
        """
        TODO
        """
        return self._gain_to_noise_temperature

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Frequency",
                    "unit": "GHz",
                    "value": self.frequency,
                },
                {
                    "name": "Wavelength",
                    "unit": "m",
                    "value": self.wavelength,
                },
                {
                    "name": "Efficiency",
                    "unit": "%",
                    "value": self.efficiency,
                },
                {
                    "name": "Feeder Loss",
                    "unit": "dB",
                    "value": watt_to_decibel(self.loss),
                },
                {
                    "name": "Gain",
                    "unit": "dB",
                    "value": watt_to_decibel(self.gain),
                },
                {
                    "name": "EIRP",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.eirp),
                },
                {
                    "name": "S/N",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.signal_to_noise),
                },
            ]
        )
        summary.set_index("name", inplace=True)

        if self._isset(self.amplifier):
            amplifier = self.amplifier.summary()
            amplifier.index = "Amplifier " + amplifier.index
            summary = pd.concat([summary, amplifier])

        if self._isset(self.modulation):
            modulation = self.modulation.summary()
            modulation.index = "Modulation " + modulation.index
            summary = pd.concat([summary, modulation])
        return summary

    def propagate_calculations(self) -> float:
        for _ in range(3):
            for var in type(self).__dict__:
                getattr(self, var)

    def _isset(self, *args) -> bool:
        return not (None in args)


class HalfWaveDipole(Antenna):
    """
    Class for omnidirectuinal radiation pattern
    """

    def __init__(
        self,
        amplifier: Amplifier = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        half_beamwidth: float = None,  # deg
    ):
        super().__init__(
            amplifier=amplifier,
            gain=gain,
            loss=loss,
            frequency=frequency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
        )

    @property
    def effective_aperture(self) -> float:
        if self._effective_aperture is None:
            self._effective_aperture = 0.13 * self.wavelength
        return self._effective_aperture

    def off_sight_gain(self, theta: float) -> float:
        """
        theta (float, deg): ??
        """
        return cos(np.pi / 2 * cos(radians(theta))) ** 2 / sin(radians(theta)) ** 2


class ConicalHornAntenna(Antenna):
    def __init__(
        self,
        amplifier: Amplifier = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        half_beamwidth: float = 20,  # deg
    ):
        super().__init__(
            amplifier=amplifier,
            gain=gain,
            loss=loss,
            frequency=frequency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
        )


class SquareHornAntenna(Antenna):
    def __init__(
        self,
        cross_sect_diameter: float,
        amplifier: Amplifier = None,
        efficiency: float = 1,
        half_beamwidth: float = None,  # deg
        gain: float = None,
        loss: float = 1,
        frequency: float = None,
        effective_aperture: float = None,
    ):
        effective_aperture = efficiency * cross_sect_diameter**2
        super().__init__(
            amplifier=amplifier,
            gain=gain,
            loss=loss,
            frequency=frequency,
            efficiency=efficiency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
            cross_sect_diameter=cross_sect_diameter,
        )

    @property
    def gain(self):
        """
        TODO
        """
        if self._gain is None:
            self._gain = (
                self.efficiency
                * 4
                * pi
                * self.cross_sect_diameter**2
                / self.wavelength**2
            )
        return self._gain

    @property
    def half_beamwidth(self) -> float:
        """
        TODO
        """
        if self._half_beamwidth is None:
            self._half_beamwidth = degrees(
                0.88 * self.wavelength / self.cross_sect_diameter
            )
        return self._half_beamwidth


class ParabolicAntenna(Antenna):
    def __init__(
        self,
        circular_diameter: float,
        amplifier: Amplifier = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        wavelength: float = None,
        effective_aperture: float = None,
        efficiency: float = None,
        beamwidth_scale_factor: float = None,
        half_beamwidth: float = None,  # deg
        roughness_factor: float = None,
        carrier_to_noise: float = None,
        signal_to_noise: float = None,
        modulation: Modulation = None,
        combined_loss: float = None,
    ):
        self._beamwidth_scale_factor = beamwidth_scale_factor
        super().__init__(
            amplifier=amplifier,
            gain=gain,
            loss=loss,
            frequency=frequency,
            wavelength=wavelength,
            efficiency=efficiency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
            cross_sect_diameter=circular_diameter,
            modulation=modulation,
            carrier_to_noise=carrier_to_noise,
            signal_to_noise=signal_to_noise,
            combined_loss=combined_loss,
        )

    @property
    def gain(self) -> float:
        """
        TODO
        """
        if self._gain is None:
            self._gain = (
                self.efficiency * (pi * self.cross_sect_diameter / self.wavelength) ** 2
            )
        return self._gain

    @property
    def cross_sect_area(self):
        """
        TODO
        """
        if self._cross_sect_area is None:
            self._cross_sect_area = pi / 4 * self.circular_diameter**2
        return self._cross_sect_area

    @property
    def half_beamwidth(self) -> float:
        """
        TODO
        """
        if self._half_beamwidth is None:
            self._half_beamwidth = self._beamwidth_scale_factor * (
                self.wavelength / self.cross_sect_diameter
            )
        return self._half_beamwidth

    def off_sight_gain(self, k: float, theta: float):
        """
        TODO
        """
        return self.gain * self.pointing_loss(theta)

    def summary(self) -> pd.DataFrame:
        summary = pd.DataFrame.from_records(
            [
                {
                    "name": "Diameter",
                    "unit": "m",
                    "value": self.cross_sect_diameter,
                },
                {
                    "name": "Gain",
                    "unit": "dB",
                    "value": watt_to_decibel(self.gain),
                },
                {
                    "name": "Half Beamwidth",
                    "unit": "dBW",
                    "value": watt_to_decibel(self.eirp),
                },
            ]
        )
        summary.set_index("name", inplace=True)

        antenna = super().summary()
        antenna.drop("Gain", inplace=True)
        summary = pd.concat([summary, antenna])
        return summary


class HelicalAntenna(Antenna):
    def __init__(
        self,
        circular_diameter: float,
        n_helix_turns: float,
        turn_spacing: float,
        amplifier: Amplifier = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        efficiency: float = None,
        half_beamwidth: float = 20,  # deg
    ):
        self.n_helix_turns = n_helix_turns
        self.turn_spacing = n_helix_turns
        super().__init__(
            amplifier=amplifier,
            gain=gain,
            loss=loss,
            frequency=frequency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
            cross_sect_diameter=circular_diameter,
        )

    @property
    def gain(self) -> float:
        """
        TODO
        """
        if self._gain is None:
            self._gain = (
                15
                * self.n_helix_turns
                * self.turn_spacing
                * (pi**2)
                * (self.cross_sect_diameter**2)
                / self.wavelength**3
            )
        return self._gain
