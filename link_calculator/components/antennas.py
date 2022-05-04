from math import cos, degrees, exp, pi, radians, sin

import numpy as np

from link_calculator.propagation.conversions import (
    frequency_to_wavelength,
    wavelength_to_frequency,
)

# from scipy.special import j1


class Antenna:
    def __init__(
        self,
        name: str,
        power: float = None,
        gain: float = None,
        loss: float = None,
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
            power (float, W): transmit/receive power of the antenna
            gain (float, W): the power gain of the antenna
            loss (float, W): the power loss of the antenna
            cross_sect_area (float, m^2): cross sectional area of the antenna aperture
            frequency (float, GHz): the transmit frequency of the antenna
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

    def max_gain(self, cross_sect_area: float = None) -> float:
        cross_sect_area = cross_sect_area if cross_sect_area else self._cross_sect_area
        wavelength = frequency_to_wavelength(self._frequency)
        return self._efficiency * 4 * np.pi * self._cross_sect_area / wavelength**2

    def half_power_beamwidth(self, cross_sect_diameter: float) -> float:
        wavelength = frequency_to_wavelength(self.frequency)
        return wavelength / (cross_sect_diameter * np.sqrt(self._efficiency))

    def power_density(self, distance: float) -> float:
        """
        Calculate the power density of the wavefront

        Parameters
        ---------
            power (float, W): the transmitted power
            gain (float, W): the power gained
            distance (float, m): the distance between the transmit and receive antennas

        Returns
        ------
            power_density (float, W/m^2): the power density at distance d
        """
        return (self._power * self._gain) / (4 * np.pi * distance**2)

    @property
    def eirp(self) -> float:
        """
        Calculate the Effetive Isotropic Radiated Power

        Parameters
        ----------
            power (float, W): the total output amplifier power
            loss (float, ): coupling loss between transmitter and antenna
                in the range [0, 1]
            gain (float, ): transmitter gain in the direction of the
                receiving antenna

        Returns
        -------
            eirp (float, dB): power incident at the receiver that would have had to be radiated
                from an isotropic antenna to achieve the same power incident at the
                receiver  as that of a transmitter with a specific antenna gain
        """
        return self._power * self._loss * self._gain

    def power_density_eirp(self, distance: float, atmospheric_loss: float) -> float:
        """
        Calculate the power density of the wavefront using EIRP

        Parameters
        ---------
            eirp (float, dB)
            distance (float, m): the distance between the transmit and receive antennas
            atmospheric_loss (float, ): the total losses due to the atmosphere

        Returns
        ------
            power_density (float, W/m^2): the power density at distance d
        """
        return self.eirp() / (4 * np.pi * distance**2) * atmospheric_loss

    @property
    def effective_aperture(self) -> float:
        """
        Calculate the effective area of the receiving antenna

        Parameters
        ----------
            gain (float, ): gain of the receive antenna
            wavelength (float, m): the radiation wavelength

        Returns
        -------
            effective_aperture (float, m^2): the effive aperture of the receive antenna
        """
        return (
            self._effective_aperture
            if self._effective_aperture is not None
            else self.__effective_aperture()
        )

    @effective_aperture.setter
    def effective_aperture(self, value):
        self._effective_aperture = value

    def __effective_aperture(self) -> float:
        return self.gain * self._wavelength**2 / (4 * np.pi)

    @property
    def directivity(self) -> float:
        """
        TODO
        """
        return 4 * pi * self._cross_sect_area / self._wavelength**2

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value

    @property
    def frequency(self):
        return (
            self._frequency
            if self._frequency is not None
            else wavelength_to_frequency(self.wavelength)
        )

    @frequency.setter
    def frequency(self, value):
        self.frequency = value

    @property
    def wavelength(self):
        return (
            self._wavelength
            if self._wavelength is not None
            else frequency_to_wavelength(self.frequency)
        )

    @wavelength.setter
    def wavelength(self, value):
        self._wavelength = value


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
        impedance: float = 73,  # Omega
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
        impedance: float = None,  # Omega
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
        half_beamwidth: float,  # deg
        cross_sect_diameter: float = None,
        power: float = None,
        gain: float = None,
        loss: float = None,
        frequency: float = None,
        effective_aperture: float = None,
        efficiency: float = None,
        impedance: float = None,  # Omega
    ):
        effective_aperture = efficiency * cross_sect_diameter**2
        super().__init__(
            name=name,
            power=power,
            gain=gain,
            loss=loss,
            frequency=frequency,
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
            cross_sect_diameter=cross_sect_diameter,
        )

    @property
    def gain(self):
        """
        TODO
        """
        return self.gain if self.gain is not None else self._gain()

    def _gain(self) -> float:
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

    def half_beamwidth(self):
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
        impedance: float = None,  # Omega
        half_beamwidth: float = 20,  # deg
    ):
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
        return self.gain if self._gain is not None else self.__gain()

    def __gain(self) -> float:
        """
        TODO
        """
        return (
            self._efficiency * (pi * self._cross_sect_diameter / self._wavelength) ** 2
        )

    def half_power_beamwidth(self, k: float):
        """
        TODO
        """
        return (
            self.half_beamwidth
            if self.half_beamwidth is None
            else self._half_beamwidth(k)
        )

    def _half_beamwidth(self, k: float) -> float:
        """
        TODO
        """
        return k * (self.wavelength / self.cross_sect_diameter)

    def off_sight_gain(self, k: float, theta: float):
        """
        TODO
        """
        return self.gain * self.pointing_loss(k, theta)

    def pointing_loss(self, k: float, theta: float) -> float:
        """
        TODO
        """
        return exp(-2.26 * (radians(theta) / self.half_power_beamwidth(k)) ** 2)


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
        impedance: float = None,  # Omega
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
        return self.gain if self._gain is not None else self.__gain()

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
