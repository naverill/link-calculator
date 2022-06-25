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
        radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        mean_motion: float = None,
        flight_path_angle: float = None,
        specific_momentum: float = None,
        periapsis_radius: float = None,
        apoapsis_radius: float = None,
        eccentric_anomaly: float = None,
        time_since_periapsis: float = None,
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
        self._radius = radius
        self._mu = mu
        self._specific_energy = specific_energy
        self._velocity = velocity
        self._specific_momentum = specific_momentum
        self._escape_velocity = escape_velocity
        self._flight_path_angle = flight_path_angle
        self._mean_motion = mean_motion
        self._periapsis_radius = periapsis_radius
        self._apoapsis_radius = apoapsis_radius
        self._time_since_periapsis = time_since_periapsis
        self._eccentric_anomaly = eccentric_anomaly
        self.propagate_calculations()

    @property
    def semimajor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semimajor_axis is None:
            if self._isset(self._specific_energy):
                # (2.10)
                self._semimajor_axis = -self.mu / (2 * self.specific_energy)
        return self._semimajor_axis

    @property
    def semiminor_axis(self) -> float:
        return self._semiminor_axis

    @property
    def mu(self) -> float:
        return self._mu

    @property
    def flight_path_angle(self) -> float:
        return self._flight_path_angle

    @property
    def radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._radius is None:
            if self._isset(
                self._eccentricity, self._true_anomaly, self._semimajor_axis
            ):
                # (2.22)
                self._radius = (
                    self.semimajor_axis
                    * (1 - self.eccentricity**2)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
        return self._radius

    @property
    def eccentricity(self) -> float:
        if self._eccentricity is None:
            if self._isset(self._specific_momentum, self._semimajor_axis):
                self._eccentricity = sqrt(
                    1 - self.specific_momentum**2 / (self.mu * self.semimajor_axis)
                )
        return self._eccentricity

    @property
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
                self._specific_energy = self.velocity**2 / 2 - self.mu / self.radius
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
            if self._isset(self._specific_energy, self._radius):
                # (2.8)
                self._velocity = sqrt(
                    2 * (self.specific_energy + self.mu / self.radius)
                )
            elif self._isset(self._radius, self._semimajor_axis):
                # (2.14)
                self._velocity = sqrt(
                    (2 * self.mu / self.radius - self.mu / self.semimajor_axis)
                )
        return self._velocity

    @property
    def specific_momentum(self) -> float:
        if self._specific_momentum is None:
            if self._isset(self._radius, self._velocity, self._flight_path_angle):
                self._specific_momentum = (
                    self.radius * self.velocity * cos(radians(self.flight_path_angle))
                )
        return self._specific_momentum

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
        radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        periapsis_radius: float = None,
        escape_velocity: float = None,
        apoapsis_radius: float = None,
        flight_path_angle: float = None,
        mean_motion: float = None,
        specific_momentum: float = None,
        eccentric_anomaly: float = None,
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
            radius=radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mean_motion=mean_motion,
            escape_velocity=escape_velocity,
            flight_path_angle=flight_path_angle,
            specific_momentum=specific_momentum,
            periapsis_radius=periapsis_radius,
            apoapsis_radius=apoapsis_radius,
            eccentric_anomaly=eccentric_anomaly,
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
                    np.sqrt(self.semimajor_axis**2 - self.semiminor_axis**2)
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
            elif self._isset(self._specific_momentum, self._semimajor_axis):
                self._eccentricity = sqrt(
                    1 - self.specific_momentum**2 / (self.mu * self.semimajor_axis)
                )
        return self._eccentricity

    @staticmethod
    def transfer_eccentricity(
        radius1: float, true_anomaly1: float, radius2: float, true_anomaly2: float
    ) -> float:
        """
        Calculate the eccentricity of an elliptical orbit between two given
        points
        """
        return (radius2 - radius1) / (
            radius1 * cos(radians(true_anomaly1))
            - radius2 * cos(radians(true_anomaly2))
        )

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
    def radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._radius is None:
            if self._isset(
                self._semimajor_axis, self._eccentricity, self._true_anomaly
            ):
                # (2.22)
                self._radius = (
                    self.semimajor_axis
                    * (1 - self.eccentricity**2)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
            elif self._isset(self._eccentricity, self._periapsis_radius):
                # (2.23)
                self._radius = (
                    self.periapsis_radius
                    * (1 + self.eccentricity)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
        return self._radius

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
            elif self._isset(self._periapsis_radius, self._eccentricity):
                # (2.43)
                self._apoapsis_radius = (
                    self.periapsis_radius
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
            elif self._isset(self._radius, self._eccentricity, self._true_anomaly):
                # (2.29)
                self._periapsis_radius = (
                    self.radius
                    * (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                    / (1 + self.eccentricity)
                )
        return self._periapsis_radius

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
            elif self._isset(self._velocity, self._radius):
                # (2.47)
                self._semimajor_axis = (self.mu * self.radius) / (
                    2 * self.mu - self.velocity**2 * self.radius
                )
            elif self._isset(self._periapsis_radius, self._eccentricity):
                # (2.48)
                self._semimajor_axis = self.periapsis_radius / (1 - self.eccentricity)
            elif self._isset(self._apoapsis_radius, self._eccentricity):
                # (2.49)
                self._semimajor_axis = self.apoapsis_radius / (1 + self.eccenticity)
        return self._semimajor_axis

    @property
    def true_anomaly(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._true_anomaly is None:
            if self._isset(self._periapsis_radius, self._eccentricity, self._radius):
                # (2.24)
                self._true_anomaly = degrees(
                    acos(
                        self.periapsis_radius
                        * (1 + self.eccentricity)
                        / (self.radius * self.eccentricity)
                        - (1 / self.eccentricity)
                    )
                )
            elif self._isset(self._semimajor_axis, self._eccentricity, self._radius):
                # (2.25)
                self._true_anomaly = degrees(
                    acos(
                        self.semimajor_axis
                        * (1 - self.eccentricity**2)
                        / (self.radius * self.eccentricity)
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
            if self._isset(self._radius, self._semimajor_axis):
                # (2.14)
                print(self.radius, self.mu, self.semimajor_axis)
                self._velocity = sqrt(
                    2 * self.mu / self.radius - self.mu / self.semimajor_axis
                )
        return self._velocity

    @property
    def time_since_periapsis(self) -> float:
        """
        The time taken by a spacecraft to move from periapsis
        to a given true anomaly

        Equations from Spacecraft Mission Design (1998)
        """
        if self._time_since_periapsis is None:
            if self._isset(
                self._mean_motion, self._eccentric_anomaly, self._eccentricity
            ):
                # (2.34)
                self._time_since_periapsis = (
                    radians(self.eccentric_anomaly)
                    - self.eccentricity * sin(radians(self.eccentric_anomaly))
                ) / self.mean_motion
        return self._time_since_periapsis

    @property
    def eccentric_anomaly(self) -> float:
        """
        The eccentric anomaly traces a point on a circle, with radius equal to a,
        that circumscribes the elliptical orbit.

        Equations from Spacecraft Mission Design (1998)
        """
        if self._eccentric_anomaly is None:
            if self._isset(self._eccentricity, self._true_anomaly):
                # (2.35)
                self._eccentric_anomaly = degrees(
                    acos(
                        (self.eccentricity + cos(radians(self.true_anomaly)))
                        / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                    )
                )
        return self._eccentric_anomaly


class CircularOrbit(EllipticalOrbit):
    def __init__(
        self,
        semimajor_axis: float = None,
        semiminor_axis: float = None,
        eccentricity: float = 0,
        inclination: float = float,
        raan: float = None,
        arg_of_periapsis: float = None,
        true_anomaly: float = None,
        period: float = None,
        radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        flight_path_angle: float = None,
        specific_momentum: float = None,
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
            radius=radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mu=mu,
            escape_velocity=escape_velocity,
            specific_momentum=specific_momentum,
            flight_path_angle=flight_path_angle,
        )

    @property
    def velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._radius):
                # (2.6)
                self._velocity = sqrt(self.mu / self.radius)
        return self._velocity

    @property
    def escape_velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._escape_velocity is None:
            if self._isset(self._radius):
                # (2.15)
                self.__escape_velocity = sqrt(2 * self.mu / self.radius)
        return self._escape_velocity

    @property
    def radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._radius is None:
            if self._isset(self._period):
                # (2.51)
                self._radius = ((self.period**2 * self.mu) / (4 * pi**2)) ** (1 / 3)
            elif self._isset(self._semimajor_axis):
                self._radius = self.semimajor_axis
            elif self._isset(self._semiminor_axis):
                self._radius = self.semiminor_axis
        return self._radius

    @property
    def semimajor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semimajor_axis is None:
            if self._isset(self._radius):
                self._semimajor_axis = self.radius
            elif self._isset(self._semiminor_axis):
                self._semimajor_axis = self.semiminor_axis
        return self._semimajor_axis

    @property
    def semiminor_axis(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._semiminor_axis is None:
            if self._isset(self._radius):
                self._semiminor_axis = self.radius
            elif self._isset(self._semimajor_axis):
                self._semiminor_axis = self.semimajor_axis
        return self._semiminor_axis

    @property
    def period(self) -> float:
        """
        Calculate the period of the satellite's orbit according to Kepler's third law

            mu (float, km^3/s^-2, optional): Kepler's gravitational constant

        Returns
        ------
            period (float, s): the time taken for the satellite to complete a revolution

        Equations from Spacecraft Mission Design (1998)
        """
        if self._period is None:
            if self._isset(self._semimajor_axis):
                self._period = 2 * pi * sqrt(self.semimajor_axis**3 / self.mu)
        return self._period


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
        radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        specific_momentum: float = None,
        flight_path_angle: float = None,
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
            radius=radius,
            specific_energy=specific_energy,
            velocity=velocity,
            mu=mu,
            specific_momentum=specific_momentum,
            escape_velocity=escape_velocity,
            flight_path_angle=flight_path_angle,
        )

    @property
    def velocity(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._radius):
                self._velocity = sqrt(self.mu / self.radius)
        return self._velocity

    @property
    def period(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._period is not None:
            if self._isset(self._radius):
                self._period = 2 * pi * sqrt(self.radius**3 / self.mu)
        return self._period

    @property
    def radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._radius is None:
            self._radius = ((self.period**2 * self.mu) / (4 * pi**2)) ** (1 / 3)
        return self._radius


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
        radius: float = None,
        specific_energy: float = None,
        velocity: float = None,
        escape_velocity: float = None,
        angle_of_asymptote: float = None,
        asymptote_true_anomaly: float = None,
        specific_momentum: float = None,
        flight_path_angle: float = None,
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
            radius=radius,
            specific_energy=specific_energy,
            velocity=velocity,
            specific_momentum=specific_momentum,
            mu=mu,
            escape_velocity=escape_velocity,
            flight_path_angle=flight_path_angle,
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
                self._angle_of_asymptote = degrees(acos(1 / self.eccentricity))
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
                self._flight_path_angle = degrees(
                    atan2(
                        1 + self.eccentricity * cos(radians(self.true_anomaly)),
                        self.eccentricity * sin(radians(self.true_anomaly)),
                    )
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
    def radius(self) -> float:
        """
        Equations from Spacecraft Mission Design (1998)
        """
        if self._radius is None:
            if self._isset(
                self._semimajor_axis, self._eccentricity, self._true_anomaly
            ):
                # (2.51)
                self._radius = (
                    self.semimajor_axis
                    * (self.eccentricity**2 - 1)
                    / (1 + self.eccentricity * cos(radians(self.true_anomaly)))
                )
        return self._radius

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
            if self._isset(self._semimajor_axis, self._eccentricity, self._radius):
                # (2.52)
                self._true_anomaly = (
                    self.semimajor_axis
                    * (self.eccentricity**2 - 1)
                    / (self.radius * self.eccentricity)
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
                self._asymptote_true_anomaly = degrees(acos(-1 / self.eccentricity))
            if self._isset(self._angle_of_asymptote):
                # (2.53)
                self._asymptote_true_anomaly = 180 + self.angle_of_asymptote
        return self._asymptote_true_anomaly

    @property
    def velocity(self) -> float:
        """
        Velocity at any point on a hyperbola

        Equations from Spacecraft Mission Design (1998)
        """
        if self._velocity is None:
            if self._isset(self._radius, self._semimajor_axis):
                # (2.16)
                self._velocity = sqrt(
                    (2 * self.mu) / self.radius + self.mu / self.semimajor_axis
                )
            elif self._isset(self._radius, self._excess_velocity):
                # (2.57)
                self._velocity = sqrt(
                    (2 * self.mu / self.radius + self.excess_velocity**2)
                )
        return self._velocity

    @property
    def excess_velocity(self) -> float:
        """
        Voo is the velocity in excess of the escape velocity and is called the hyperbolic
        excess velocity (VHE) when Earth escape is intended

        Equations from Spacecraft Mission Design (1998)
        """
        if self._excess_velocity is None:
            if self._isset(self._semi_major_axis):
                # (2.56)
                self._excess_velocity = sqrt(self.mu / self.semi_major_axis)