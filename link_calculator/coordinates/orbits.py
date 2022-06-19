from math import acos, atan2, cos, degrees, pi, radians, sin, sqrt, tan

import numpy as np
import pandas as pd

from link_calculator.constants import EARTH_MU, EARTH_RADIUS


class Orbit:
    def __init__(
        self,
        semimajor_axis: float = None,
        semiminor_axis: float = None,
        eccentricity: float = None,
        inclination: float = float,
        raan: float = None,
        arg_of_periapsis: float = None,
        true_anomaly: float = None,
        period: float = None,
        orbital_radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        mean_motion: float = None,
        mu: float = EARTH_MU,
    ):
        """

        Parameters
        ---------
            semimajor_axis (float, km): The semi-major axis of the orbit
        """
        self._semimajor_axis = semimajor_axis
        self._semiminor_axis = semiminor_axis
        self._eccentricity = eccentricity
        self._inclination = inclination
        self._raan = raan
        self._arg_of_periapsis = arg_of_periapsis
        self._true_anomaly = true_anomaly
        self._period = period
        self._orbital_radius = orbital_radius
        self._mu = mu
        self._specific_energy = specific_energy
        self._velocity = velocity
        self._escape_velocity = escape_velocity
        self._mean_motion = mean_motion
        self.propagate_calculations()

    def period(self, mu: float = EARTH_MU) -> float:
        """
        Calculate the period of the satellite's orbit according to Kepler's third law

            mu (float, km^3/s^-2, optional): Kepler's gravitational constant

        Returns
        ------
            period (float, s): the time taken for the satellite to complete a revolution
        """
        if self._period is None:
            self._period = 2 * pi * sqrt(self.semimajor_axis**3 / mu)
        return self._period

    @property
    def semimajor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semimajor_axis is not None:
            if self._isset(self._specific_energy):
                # (2.10)
                self._semimajor_axis = -self._mu / (2 * self.specific_energy)
        return self._semimajor_axis

    @property
    def semiminor_axis(self) -> float:
        return self._semiminor_axis

    @property
    def mu(self) -> float:
        return self._mu

    @property
    def orbital_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._orbital_radius is None:
            # (2.22)
            self._orbital_radius = (
                self.semimajor_axis
                * (1 - self.eccentricity**2)
                / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
            )
        return self._orbital_radius

    def eccentricity(self) -> float:
        if self._eccentricity is None:
            if self._isset(self._semimajor_axis, self._semiminor_axis):
                self._eccentricity = (
                    np.sqrt(self.semimajor_axis**2, self.semiminor_axis**2)
                    / self.semimajor_axis
                )
        return self._eccentricity

    def specific_energy(self) -> float:
        """
        Specific orbital energy (float, J/kg = m2⋅s−2): the constant sum
            of two orbiting bodies mutual potential energy and their total
            kinetic energy divided by the reduced mass.

            Equations from Spacecraft Mission Design (1998)
        """
        if self._specific_energy is None:
            if self._isset(self._velocity, self._radius):
                # (2.8)
                self._specific_energy = (
                    self.velocity**2 / 2 - self.mu / self.orbital_radius
                )
            elif self._isset(self._semimajor_axis):
                # (2.9)
                self._specific_energy = -self.mu / (2 * self.semimajor_axis)
        return self._specific_energy

    @property
    def velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._specific_energy, self._orbital_radius):
                # (2.8)
                self._velocity = sqrt(
                    2 * (self.specific_energy + self.mu / self.orbital_radius)
                )
            elif self._isset(self._orbital_radius, self._semimajor_axis):
                # (2.14)
                self._velocity = sqrt(
                    (2 * self.mu / self.orbital_radius - self.mu / self.semimajor_axis)
                )
        return self._velocity

    def propagate_calculations(self) -> float:
        for _ in range(3):
            for var in type(self).__dict__:
                getattr(self, var)

    def _isset(self, *args) -> bool:
        return not (None in args)


class EllipticalOrbit(Orbit):
    def __init__(
        self,
        semimajor_axis: float = None,
        semiminor_axis: float = None,
        eccentricity: float = None,
        inclination: float = float,
        raan: float = None,
        arg_of_periapsis: float = None,
        true_anomaly: float = None,
        period: float = None,
        orbital_radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        periapsis_radius: float = None,
        apoapsis_radius: float = None,
        mean_motion: float = None,
        mu: float = EARTH_MU,
    ):
        super().__init__(
            semimajor_axis=semimajor_axis,
            semiminor_axis=semiminor_axis,
            eccentricity=eccentricity,
            inclination=inclination,
            raan=raan,
            arg_of_periapsis=arg_of_periapsis,
            true_anomaly=true_anomaly,
            period=period,
            orbital_radius=orbital_radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mean_motion=mean_motion,
            mu=mu,
        )

    @property
    def eccentricity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._eccentricity is None:
            if self._isset(self._semimajor_axis, self._semiminor_axis):
                self._eccentricity = (
                    np.sqrt(self.semimajor_axis**2, self.semiminor_axis**2)
                    / self.semimajor_axis
                )
            elif self._isset(self._semimajor_axis, self._apoapsis_radius):
                # (2.39)
                self._eccentricity = self.apoapsis_radius / self.semimajor_axis - 1
            elif self._isset(self._semimajor_axis, self._periapsis_radius):
                # (2.40)
                self._eccentricity = 1 - self.periapsis_radius / self.semimajor_axis
            elif self._isset(self._apoapsis_radius, self._periapsis_radius):
                # (2.20)
                self._eccentricity = (self.apoapsis_radius - self.periapsis_radius) / (
                    self.apoapsis_radius + self.periapsis_radius
                )
        return self._eccentricity

    @property
    def flight_path_angle(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._flight_path_angle is None:
            if self._isset(self._eccentricity, self._true_anomaly):
                # (2.31)
                self._flight_path_angle = atan2(
                    1 + self.eccentricity * cos(radians(self.true_anomaly)),
                    self.eccentricity * cos(radians(self.true_anomaly)),
                )
        return self._flight_path_angle

    @property
    def mean_motion(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._mean_motion is None:
            if self._isset(self._semimajor_axis):
                # (2.36)
                self._mean_motion = sqrt(self.mu / self.semimajor_axis**3)
            elif self._isset(self._period):
                # (2.37)
                self._mean_motion = 2 * pi / self.mean_motion
        return self._mean_motion

    @property
    def period(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._period is None:
            if self._isset(self._mean_motion):
                # (2.37)
                self._period = 2 * pi / self.mean_motion
            if self._isset(self._semimajor_axis):
                # (2.38)
                self._period = 2 * pi * sqrt(self.semimajor_axis / self.mu)
        return self._period

    @property
    def orbital_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._orbital_radius is None:
            if self._isset(
                self._semimajor_axis, self._eccentricity, self._true_anomaly
            ):
                # (2.22)
                self._orbital_radius = (
                    self.semimajor_axis
                    * (1 - self.eccentricity**2)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
            elif self._isset(self._eccentricity, self._periapsis_radius):
                # (2.23)
                self._orbital_radius = (
                    self.periapsis_radius
                    * (1 + self.eccentricity)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
        return self._orbital_radius

    @property
    def apoapsis_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._apoapsis_radius is None:
            if self._isset(self._semimajor_axis, self._eccentricity):
                # (2.41)
                self._apoapsis_radius = self.semimajor_axis * (1 + self.eccentricity)
            elif self._isset(self._semimajor_axis, self._periapsis_radius):
                # (2.42)
                self._apoapsis_radius = 2 * self.semimajor_axis - self.periapsis_radius
            elif self._isset(self._perigee_radius, self._eccentricity):
                # (2.43)
                self._apoapsis_radius = (
                    self.perigee_radius
                    * (1 + self.eccentricity)
                    / (1 - self.eccentricity)
                )
        return self._apoapsis_radius

    @property
    def periapsis_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._periapsis_radius is None:
            if self._isset(self._semimajor_axis, self._eccentricity):
                # (2.44)
                self._periapsis_radius = self.semimajor_axis * (1 - self.eccentricity)
            elif self._isset(self._apoapsis_radius, self._eccentricity):
                # (2.45)
                self._periapsis_radius = (
                    self.apoapsis_radius
                    * (1 - self.eccentricity)
                    * (1 + self.eccentricity)
                )
            elif self._isset(self._semimajor_axis, self._apoapsis_radius):
                # (2.46)
                self._periapsis_radius = 2 * self.semimajor_axis - self.apoasis_radius
            elif self._isset(
                self.orbital_radius, self._eccentricity, self._true_anomaly
            ):
                # (2.29)
                self._periapsis_radius = (
                    self.orbital_radius
                    * (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                    / (1 + self.eccentricity)
                )
        return self._peiapsis_radius

    @property
    def semimajor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semimajor_axis is None:
            if self._isset(self._apoapsis_radius, self._periapsis_radius):
                # (2.17)
                self._semimajor_axis = (
                    self.periapsis_radius + self.apoapsis_radius
                ) / 2
            elif self._isset(self._velocity, self._orbital_radius):
                # (2.47)
                self._semimajor_axis = (self.mu * self.orbital_radius) / (
                    2 * self.mu - self.velocity**2 * self.orbital_radius
                )
            elif self.isset(self._periapsis_radius, self._eccentricity):
                # (2.48)
                self._semimajor_axis = self.periapsis_radius * (1 - self.eccenttricity)
            elif self._isset(self._apoapsis_radius, self._eccentricity):
                # (2.49)
                self._semimajor_axis = self.apoapsis_radius * (1 + self.eccenticity)
        return self._semimajor_axis

    @property
    def true_anomaly(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._true_anomaly is None:
            if self._isset(
                self._periapsis_radius, self._eccentricity, self._orbital_radius
            ):
                # (2.24)
                self._true_anomaly = degrees(
                    acos(
                        self.periapsis_radius
                        * (1 + self.eccentricity)
                        / (self.orbital_radius * self.eccentricity)
                        - (1 / self.eccentricity)
                    )
                )
            elif self._isset(self._semimajor_axis, self._eccentricity, self._radius):
                # (2.25)
                self._true_anomaly = degrees(
                    acos(
                        self.semimajor_axis
                        * (1 - self.eccentricity**2)
                        / (self.orbital_radius * self.eccentricity)
                        - (1 / self.eccentricity)
                    )
                )
        return self._true_anomaly

    @property
    def velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._orbital_radius, self._semimajor_axis):
                # (2.14)
                self._velocity = sqrt(
                    2 * self.mu / self.orbital_radius - self.mu / self.semimajor_axis
                )
        return self._velocity

    @property
    def time_since_periapsis(self) -> float:
        # TODO
        pass


class CircularOrbit(EllipticalOrbit):
    def __init__(
        self,
        semimajor_axis: float = None,
        semiminor_axis: float = None,
        eccentricity: float = None,
        inclination: float = float,
        raan: float = None,
        arg_of_periapsis: float = None,
        true_anomaly: float = None,
        period: float = None,
        orbital_radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        mu: float = EARTH_MU,
    ):
        super().__init__(
            semimajor_axis=semimajor_axis,
            semiminor_axis=semiminor_axis,
            eccentricity=eccentricity,
            inclination=inclination,
            raan=raan,
            arg_of_periapsis=arg_of_periapsis,
            true_anomaly=true_anomaly,
            period=period,
            orbital_radius=orbital_radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mu=mu,
            escape_velocity=escape_velocity,
        )

    @property
    def velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._orbital_radius):
                # (2.6)
                self._velocity = sqrt(self.mu / self.orbital_radius)
        return self._velocity

    @property
    def escape_velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self.__escape_velocity is None:
            if self._isset(self._orbital_radius):
                # (2.15)
                self.__escape_velocity = sqrt(2 * self.mu / self.orbital_radius)
        return self._escape_velocity

    @property
    def period(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._period is not None:
            if self._isset(self._orbital_radius):
                # (2.7)
                self._period = 2 * pi * sqrt(self.orbital_radius**3 / self.mu)
        return self._period

    @property
    def orbital_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._orbital_radius is None:
            if self._isset(self._period):
                # (2.51)
                self._orbital_radius = (
                    (self.period**2 * self.mu) / (4 * pi**2)
                ) ** (1 / 3)
            elif self._isset(self._semimajor_axis):
                self._orbital_radius = self._semimajor_axis
            elif self._isset(self._semiminor_axis):
                self._orbital_radius = self.semiminor_axis
        return self._orbital_radius

    @property
    def semimajor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semimajor_axis is None:
            if self._isset(self._orbital_radius):
                self._semimajor_axis = self.orbital_radius
            elif self._isset(self._semiminor_axis):
                self._semimajor_axis = self.semiminor_axis
        return self._semimajor_axis

    @property
    def semiminor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semiminor_axis is None:
            if self._isset(self._orbital_radius):
                self._semiminor_axis = self.orbital_radius
            elif self._isset(self._semimajor_axis):
                self._semiminor_axis = self.semimajor_axis
        return self._semiminor_axis


class ParabolicOrbit(Orbit):
    def __init__(
        self,
        semimajor_axis: float = None,
        semiminor_axis: float = None,
        eccentricity: float = None,
        inclination: float = float,
        raan: float = None,
        arg_of_periapsis: float = None,
        true_anomaly: float = None,
        period: float = None,
        orbital_radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        mu: float = EARTH_MU,
    ):
        super().__init__(
            semimajor_axis=semimajor_axis,
            semiminor_axis=semiminor_axis,
            eccentricity=eccentricity,
            inclination=inclination,
            raan=raan,
            arg_of_periapsis=arg_of_periapsis,
            true_anomaly=true_anomaly,
            period=period,
            orbital_radius=orbital_radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mu=mu,
            escape_velocity=escape_velocity,
        )

    @property
    def velocity(self) -> float:
        if self._velocity is None:
            if self._isset(self._orbital_radius):
                self._velocity = sqrt(self.mu / self.orbital_radius)
        return self._velocity

    @property
    def period(self) -> float:
        if self._period is not None:
            if self._isset(self._orbital_radius):
                self._period = 2 * pi * sqrt(self.orbital_radius**3 / self.mu)
        return self._period

    @property
    def orbital_radius(self) -> float:
        if self._orbital_radius is None:
            self._orbital_radius = ((self.period**2 * self.mu) / (4 * pi**2)) ** (
                1 / 3
            )
        return self._orbital_radius


class HyperbolicOrbit(Orbit):
    def __init__(
        self,
        semimajor_axis: float = None,
        semiminor_axis: float = None,
        eccentricity: float = None,
        inclination: float = float,
        raan: float = None,
        arg_of_periapsis: float = None,
        true_anomaly: float = None,
        period: float = None,
        orbital_radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        angle_of_asymptote: float = None,
        asymptote_true_anomaly: float = None,
        mu: float = EARTH_MU,
    ):
        self._angle_of_asymptote = self._angle_of_asymptote
        self._asymptote_true_anomaly = asymptote_true_anomaly
        super().__init__(
            semimajor_axis=semimajor_axis,
            semiminor_axis=semiminor_axis,
            eccentricity=eccentricity,
            inclination=inclination,
            raan=raan,
            arg_of_periapsis=arg_of_periapsis,
            true_anomaly=true_anomaly,
            period=period,
            orbital_radius=orbital_radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mu=mu,
            escape_velocity=escape_velocity,
        )

    @property
    def angle_of_asymptote(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._angle_of_asymptote is None:
            if self._isset(self._semimajor_axis, self._semiminor_axis):
                # (2.63)
                self._angle_of_asymptote = degrees(
                    atan2(self.semimajor_axis, self.semiminor_axis)
                )
            elif self._isset(self._eccentricity):
                # (2.50)
                self._angle_of_asymptote = acos(1 / self.eccentricity)
            elif self._isset(self._semiminor_axis, self._periapsis_radius):
                # (2.65)
                self._angle_of_asymptote = (
                    2
                    * self.semiminor_axis
                    * self.periapsis_radius
                    / (self.semiminor_axis**2 * self.periapsis_radius**2)
                )
        return self._angle_of_asymptote

    @property
    def eccentricity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._eccentricity is None:
            if self._isset(self._angle_of_asymptote):
                # (2.66)
                self._eccentricity = 1 / cos(radians(self.angle_of_asymptote))
            elif self._isset(self._semimajor_axis, self._periapsis_radius):
                # (2.67)
                self._eccentricity = 1 + self.periapsis_radius / self.semimajor_axis
            elif self._isset(self._semimajor_axis, self._semiminor_axis):
                # (2.68)
                self._eccentricity = sqrt(
                    1 + self.semiminor_axis**2 / self.semimajor_axis**2
                )
        return self._eccentricity

    @property
    def flight_path_angle(self):
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._flight_path_angle is None:
            if self._isset(self._eccentriciy, self._true_anomaly):
                # (2.31)
                self._flight_path_angle = atan2(
                    1 + self.eccentricity * cos(radians(self.true_anomaly)),
                    self.eccentricity * sin(radians(self.true_anomaly)),
                )
        return self._flight_path_angle

    @property
    def mean_motion(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._mean_motion is None:
            if self._isset(self._semimajor_axis):
                # (2.36)
                self._mean_motion = sqrt(self.mu / self.semimajor_axis**3)
        return self._mean_motion

    @property
    def orbital_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._orbital_radius is None:
            if self._isset(
                self._semimajor_axis, self._eccentricity, self._true_anomaly
            ):
                # (2.51)
                self._orbital_radius = (
                    self.semimajor_axis
                    * (self.eccentricity**2 - 1)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
        return self._orbital_radius

    @property
    def periapsis_radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._periapsis_radius is None:
            if self._isset(self._semiminor_axis, self._eccentricity):
                # (2.69)
                self._periapsis_radius = self.semiminor_axis * sqrt(
                    (self.eccentricity - 1) / (self.eccentricity + 1)
                )
            elif self._isset(self._semimajor_axis, self._eccentricity):
                # (2.70)
                self._periapsis_radius = self.semimajor_axis * (self.eccentricity - 1)
            elif self._isset(self._semiminor_axis, self._angle_of_asymptote):
                # (2.72)
                self._periapsis_radius = self.semiminor_axis * tan(
                    radians(self.angle_of_asymptote / 2)
                )
            elif self._isset(self._semimajor_axis, self._semiminor_axis):
                # (2.75)
                self._periapsis_radius = -self.semi_major_axis + sqrt(
                    self.semimajor_axis**2 + self.semiminor_axis**2
                )
            # TODO (2.73)
            # TODO (2.44)
        return self._periapsis_radius

    @property
    def semimajor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semimajor_axis is None:
            if self._isset(self._eccentricity, self._semiminor_axis):
                # (2.76)
                self._semimajor_axis = self.semiminor_axis / sqrt(
                    self.eccentricity**2 - 1
                )
            elif self._isset(self._periapsis_radius, self._eccentricity):
                # (2.77)
                self._semimajor_axis = self.periapsis_radius / (self.eccentricity - 1)
            elif self._isset(self._semiminor_axis, self._periapsis_radius):
                # (2.79)
                self._semimajor_axis = (
                    self.semiminor_axis**2 - self.periapsis_radius**2
                ) / (2 * self.periapsis_radius)
            # TODO (2.78)
            # TODO (2.80)
        return self._semimajor_axis

    @property
    def semiminor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semiminor_axis is None:
            if self._isset(self._periapsis_radius, self._eccentricity):
                # (2.81)
                self._semiminor_axis = self.periapsis_radius * sqrt(
                    (self.eccentricity + 1) / (self.eccentricity - 1)
                )
            elif self._isset(self._semimajor_axis, self._eccentricity):
                # (2.82)
                self._semiminor_axis = self.semimajor_axis * sqrt(
                    self.eccentricity**2 - 1
                )
        # TODO (2.83)
        return self._semiminor_axis

    @property
    def time_since_periapsis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        # TODO
        pass

    @property
    def true_anomaly(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._true_anomaly is None:
            if self._isset(
                self._semimajor_axis, self._eccentricity, self._orbital_radius
            ):
                # (2.52)
                self._true_anomaly = (
                    self.semimajor_axis
                    * (self.eccentricity**2 - 1)
                    / (self.orbital_radius * self.eccentricity)
                    - 1 / self.eccenricity
                )
        return self._true_anomaly

    @property
    def asymptote_true_anomaly(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._asymptote_true_anomaly is None:
            if self._isset(self._eccentricity):
                # (2.54)
                self._asymptote_true_anomaly = acos(-1 / self.eccentricity)
            # TODO (2.53)
        return self._asymptote_true_anomaly

    @property
    def velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._orbital_radius, self._semimajor_axis):
                # (2.16)
                self._velocity = sqrt(
                    (2 * self.mu) / self.orbital_radius + self.mu / self.semimajor_axis
                )
            # TODO (2.56)
            # TODO (2.57)
            # TODO (2.58)
        return self._velocity