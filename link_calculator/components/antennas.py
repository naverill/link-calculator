from math import cos, degrees, exp, pi, radians, sin

import numpy as np

from link_calculator.propagation.conversions import (
    frequency_to_wavelength,
    wavelength_to_frequency,
)


class Antenna:
    def __init__(
        self,
        name: str,
        power: float = None,
        gain: float = None,
        loss: float = 1,
        frequency: float = None,
        wavelength: float = None,
        effective_aperture: float = None,
        cross_sect_area: float = None,
        cross_sect_diameter: float = None,
        half_beamwidth: float = None,
        efficiency: float = None,
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
        """
        self._power = power
        self._gain = gain
        self._loss = loss
        self._efficiency = efficiency
        self._half_beamwidth = half_beamwidth
        self._cross_sect_area = cross_sect_area
        self._cross_sect_diameter = cross_sect_diameter
        self._frequency = frequency
        self._wavelength = wavelength
        self._effective_aperture = effective_aperture

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
            gain (float, W): the power gained
            distance (float, km): the distance between the transmit and receive antennas

        Returns
        ------
            power_density (float, W/m^2): the power density at distance d
        """
        distance = distance * 1000  # convert to m
        return (self._power * self._gain) / (4 * np.pi * distance**2)

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
        return self._power * self._loss * self._gain

    @property
    def half_beamwidth(self) -> float:
        if self._half_beamwidth is None:
            self._half_beamwidth = self.__half_beamwidth()
        return self._half_beamwidth

    def __half_beamwidth(self) -> float:
        return self.wavelength / (self._cross_sect_diameter * np.sqrt(self.efficiency))

    @half_beamwidth.setter
    def half_beamwidth(self, value):
        self.half_beamwidth = value

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
            self._effective_aperture = self.__effective_aperture()
        return self._effective_aperture

    @effective_aperture.setter
    def effective_aperture(self, value):
        self._effective_aperture = value

    def __effective_aperture(self) -> float:
        return self.gain * self.wavelength**2 / (4 * np.pi)

    @property
    def directive_gain(self) -> float:
        return self.gain / self.efficiency

    @property
    def directivity(self) -> float:
        """
        TODO
        """
        return 4 * pi * self._cross_sect_area / self.wavelength**2

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

    @property
    def gain(self):
        if self._gain is None:
            self._gain = self.__gain()
        return self._gain

    def __gain(self) -> float:
        return (
            self.efficiency * 4 * np.pi * self._cross_sect_area / self.wavelength**2
        )

    @gain.setter
    def gain(self, value):
        self._gain = value

    @property
    def frequency(self):
        if self._frequency is None:
            self._frequency = wavelength_to_frequency(self._wavelength)
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self.frequency = value

    @property
    def wavelength(self):
        if self._wavelength is None:
            self._wavelength = frequency_to_wavelength(self._frequency)
        return self._wavelength

    @wavelength.setter
    def wavelength(self, value):
        self._wavelength = value

    @property
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = value

    @property
    def cross_sect_diameter(self):
        return self._cross_sect_diameter

    @cross_sect_diameter.setter
    def cross_sect_diameter(self, value):
        self._cross_sect_diameter = value

    @property
    def loss(self):
        return self._loss

    @loss.setter
    def loss(self, value):
        self._loss = value

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


class HalfWaveDipole(Antenna):
    """
    Class for omnidirectuinal radiation pattern
    """

    def __init__(
        self,
        name: str,
        power: float = None,
        gain: float = 1.64,
        loss: float = None,
        frequency: float = None,
        half_beamwidth: float = 78,  # deg
    ):
        effective_aperture = 0.13 * frequency_to_wavelength(frequency)
        super().__init__(
            name=name,
            power=power,
            gain=gain,
            loss=loss,
            frequency=frequency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
        )

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
            self._gain = self.__gain()
        return self._gain

    def __gain(self) -> float:
        """
        TODO
        """
        return (
            self.efficiency
            * 4
            * pi
            * self.cross_sect_diameter**2
            / self.wavelength**2
        )

    @property
    def half_beamwidth(self) -> float:
        if self._half_beamwidth is None:
            self._half_beamwidth = self.__half_beamwidth()
        return self._half_beamwidth

    def __half_beamwidth(self):
        """
        TODO
        """
        return degrees(0.88 * self.wavelength / self.cross_sect_diameter)


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
            self._gain = self.__gain()
        return self._gain

    def __gain(self) -> float:
        """
        TODO
        """
        return self.efficiency * (pi * self._cross_sect_diameter / self.wavelength) ** 2

    @property
    def half_beamwidth(self) -> float:
        if self._half_beamwidth is None:
            self._half_beamwidth = self.__half_beamwidth()
        return self._half_beamwidth

    def __half_beamwidth(self) -> float:
        """
        TODO
        """
        return self._beamwidth_scale_factor * (
            self.wavelength / self.cross_sect_diameter
        )

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
            self._gain = self.__gain()
        return self._gain

    def __gain(self) -> float:
        """
        TODO
        """
        return (
            15
            * self.n_helix_turns
            * self.turn_spacing
            * (pi**2)
            * (self.cross_sect_diameter**2)
            / self.wavelength**3
        )
