from math import cos, degrees, exp, pi, radians, sin

import numpy as np

from link_calculator.constants import BOLTZMANN_CONSTANT
from link_calculator.propagation.conversions import (
    frequency_to_wavelength,
    wavelength_to_frequency,
)
from link_calculator.signal_processing.modulation import Modulation


class Amplifier:
    def __init__(self, power: float, gain: float, noise_power):
        self.power = power
        self.gain = gain
        self.noise_power = noise_power


class Antenna:
    def __init__(
        self,
        name: str,
        power: float = None,
        gain: float = None,
        loss: float = 1,
        back_off_loss: float = 1,
        feeder_loss: float = 1,
        frequency: float = None,
        wavelength: float = None,
        modulation: Modulation = None,
        effective_aperture: float = None,
        cross_sect_area: float = None,
        cross_sect_diameter: float = None,
        half_beamwidth: float = None,
        efficiency: float = None,
        roughness_factor: float = None,
        noise_temperature: float = None,
        low_noise_amp_gain: float = None,
        combined_gain: float = None,
        carrier_to_noise: float = None,
        carrier_power: float = None,
        receive_carrier_power: float = None,
        gain_to_equiv_noise_temp: float = None,
    ):
        """
        Instantiate an Antenna object

        Parameters
        ----------
            name (str): Name of antenna
            power (float, W): the total output amplifier power
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
            noise_temperature (float, Kelvin): the temperature of the environment
        """
        self._power = power
        self._gain = gain
        self._loss = loss
        self._back_off_loss = back_off_loss
        self._feeder_loss = feeder_loss
        self._efficiency = efficiency
        self._half_beamwidth = half_beamwidth
        self._cross_sect_area = cross_sect_area
        self._cross_sect_diameter = cross_sect_diameter
        self._frequency = frequency
        self._wavelength = wavelength
        self._modulation = modulation
        self._effective_aperture = effective_aperture
        self._roughness_factor = roughness_factor
        self._noise_temperature = noise_temperature
        self._low_noise_amp_gain = low_noise_amp_gain
        self._combined_gain = combined_gain
        self._carrier_to_noise = carrier_to_noise
        self._gain_to_equiv_noise_temp = gain_to_equiv_noise_temp
        self._carrier_power = carrier_power

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

    def power_density(self, distance: float) -> float:
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
        return (self.power * self.gain) / (4 * np.pi * distance**2)

    @property
    def noise_power(self) -> float:
        """
        Returns
        ----------
            noise_power (float, ): sum of the input noise power and the noise power
                added by the amplifier
        """
        if self._noise_power is None:
            self._noise_power = self.noise_density * self.bandwidth * 1e9
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
                self.noise_power / (self.bandwidth * 1e9)
            ) / BOLTZMANN_CONSTANT
        return self._noise_temperature

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
        return self.power * self.loss * self.gain

    @property
    def half_beamwidth(self) -> float:
        if self._half_beamwidth is None:
            self._half_beamwidth = self.wavelength / (
                self.cross_sect_diameter * np.sqrt(self.efficiency)
            )
        return self._half_beamwidth

    @half_beamwidth.setter
    def half_beamwidth(self, value):
        self.half_beamwidth = value

    @property
    def carrier_to_noise(self) -> float:
        if self._carrier_to_noise is None:
            self._carrier_to_noise = self.carrier_power / self.noise_density
        return self._carrier_to_noise

    @property
    def gain_to_noise_temp(self) -> float:
        if self._gain_to_noise_temp is None:
            self._gain_to_noise_temp = (self.carrier_power * BOLTZMANN_CONSTANT) / (
                self.noise_density * self.receive_carrier_power
            )
        return self._gain_to_noise_ratio

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

    @effective_aperture.setter
    def effective_aperture(self, value):
        self._effective_aperture = value

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
            self._gain = (
                self.efficiency
                * 4
                * np.pi
                * self.cross_sect_area
                / self.wavelength**2
            )
        return self._gain

    @gain.setter
    def gain(self, value):
        """
        TODO
        """
        self._gain = value

    @property
    def combined_gain(self) -> float:
        if self._combined_gain is None:
            self._combined_gain = self.amplifier.gain * self.gain
        return self._combined_gain

    @property
    def carrier_power(self) -> float:
        return self._carrier_power

    @property
    def power(self) -> float:
        """
        TODO
        Returns
        -------
            power (float, W): the total output amplifier power
        """
        return self._power

    @power.setter
    def power(self, value) -> float:
        self._power = value

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

    @frequency.setter
    def frequency(self, value):
        """
        TODO
        """
        self.frequency = value

    @property
    def wavelength(self):
        """
        TODO
        """
        if self._wavelength is None:
            self._wavelength = frequency_to_wavelength(self._frequency)
        return self._wavelength

    @wavelength.setter
    def wavelength(self, value):
        """
        TODO
        """
        self._wavelength = value

    @property
    def efficiency(self):
        """
        TODO
        """
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        """
        TODO
        """
        self._efficiency = value

    @property
    def cross_sect_diameter(self):
        """
        TODO
        """
        return self._cross_sect_diameter

    @cross_sect_diameter.setter
    def cross_sect_diameter(self, value):
        """
        TODO
        """
        self._cross_sect_diameter = value

    @property
    def cross_sect_area(self):
        """
        TODO
        """
        return self._cross_sect_area

    @cross_sect_area.setter
    def cross_sect_area(self, value):
        """
        TODO
        """
        self._cross_sect_area = value

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
            self._loss = self.back_off_loss * self.feeder_loss
        return self._loss

    @loss.setter
    def loss(self, value):
        """
        TODO
        """
        self._loss = value

    @property
    def back_off_loss(self):
        """
        TODO
        Returns
        -------
            back_off_loss (float, ): the transmit back-off loss
        """
        return self._back_off_loss

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

    @roughness_factor.setter
    def roughness_factor(self, value):
        """
        TODO
        """
        self._roughness_factor = value


class HalfWaveDipole(Antenna):
    """
    Class for omnidirectuinal radiation pattern
    """

    def __init__(
        self,
        name: str,
        power: float = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        half_beamwidth: float = None,  # deg
    ):
        super().__init__(
            name=name,
            power=power,
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
        name: str,
        power: float = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        half_beamwidth: float = 20,  # deg
    ):
        super().__init__(
            name=name,
            power=power,
            gain=gain,
            loss=loss,
            frequency=frequency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
        )


class SquareHornAntenna(Antenna):
    def __init__(
        self,
        name: str,
        cross_sect_diameter: float,
        efficiency: float = 1,
        half_beamwidth: float = None,  # deg
        power: float = None,
        gain: float = None,
        loss: float = 1,
        frequency: float = None,
        effective_aperture: float = None,
    ):
        effective_aperture = efficiency * cross_sect_diameter**2
        super().__init__(
            name=name,
            power=power,
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
        name: str,
        circular_diameter: float,
        power: float = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        efficiency: float = None,
        beamwidth_scale_factor: float = None,
        half_beamwidth: float = 20,  # deg
    ):
        self._beamwidth_scale_factor = beamwidth_scale_factor
        super().__init__(
            name=name,
            power=power,
            gain=gain,
            loss=loss,
            frequency=frequency,
            efficiency=efficiency,
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

    @cross_sect_area.setter
    def cross_sect_area(self, value) -> float:
        """
        TODO
        """
        self._cross_sect_area = value

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


class HelicalAntenna(Antenna):
    def __init__(
        self,
        name: str,
        circular_diameter: float,
        n_helix_turns: float,
        turn_spacing: float,
        power: float = None,
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
            name=name,
            power=power,
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
