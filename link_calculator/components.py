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
        loss: float = None,
        frequency: float = None,
        wavelength: float = None,
        effective_aperture: float = None,
        cross_sect_area: float = None,
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
        self.power = power
        self.gain = gain
        self.loss = loss
        self.efficiency = efficiency
        self.frequency = frequency if frequency else wavelength_to_frequency(wavelength)
        self.wavelength = (
            wavelength if wavelength else frequency_to_wavelength(frequency)
        )
        self.effective_aperture = (
            effective_aperture if effective_aperture else self.effective_aperture()
        )
        self.cross_sect_area = cross_sect_area

    def max_gain(self, cross_sect_area: float = None) -> float:
        cross_sect_area = cross_sect_area if cross_sect_area else self.cross_sect_area
        wavelength = frequency_to_wavelength(self.frequency)
        return self.efficiency * 4 * np.pi * self.cross_sect_area / wavelength**2

    def half_power_beamwidth(self, cross_sect_diameter: float) -> float:
        wavelength = frequency_to_wavelength(self.frequency)
        return wavelength / (cross_sect_diameter * np.sqrt(self.efficiency))

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
        return (self.power * self.gain) / (4 * np.pi * distance**2)

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
        return self.power * self.loss * self.gain

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
        return self.gain * self.wavelength**2 / (4 * np.pi)


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


class SquarePyramidalHornAntenna(Antenna):
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

    def half_beamwidth(self):
        return degrees(0.88 * self.wavelength / self.cross_sect_diameter)


class ParabolicReflectorAntenna(Antenna):
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
            effective_aperture=effective_aperture,
            half_beamwidth=half_beamwidth,
            cross_sect_diameter=circular_diameter,
        )

    def gain(self):
        return self.efficiency * (pi * self.cross_sect_diameter / self.wavelength) ** 2

    def half_power_beamwidth(self, k: float):
        return k * (self.wavelength / self.cross_sect_diameter)

    def off_sight_gain(self, k: float, theta: float):
        return (
            self.efficiency
            * (pi * self.cross_sect_diameter / self.wavelength)
            * exp(-2.26 * (radians(theta) / self.half_power_beamwidth(k)) ** 2)
        )


class GroundStation:
    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
        antenna: Antenna,
    ):
        """

        Parameters
        ----------
            name (str,): name of the ground station
            latitude (str, deg): the latitude of the groundstation
            longitude (str, deg): the longitude of the groundstation
            altitude (str, km): the altitude of the groundstation above sea level
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.antenna = antenna


class Satellite:
    def __init__(self, name: str, antenna: Antenna):
        self.name = name
        self.antenna = antenna
