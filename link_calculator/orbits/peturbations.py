from math import cos

from constants import SPEED_OF_LIGHT


def rate_of_precession(orbital_radius: float, inclination: float) -> float:
	"""
	Rate of rotation of orbital plane around the Earth's north-south axis 

	Parameters
	---------
		inclination (float, rad): inclination of orbit
		orbital_radius (float, km): height of orbiting body above centre of mass 

	"""
	return 2.0617 * r ** (-3.5) * cos(inclination) * 10e14


def doppler_shift_wav(rel_radial_velocity: float, wavelength: float) -> float:
	return rel_radial_velocity / wavelength


def doppler_shift_freq(rel_radial_velocity: float, frequency: float) -> float:
	return (rel_radial_velocity / SPEED_OF_LIGHT) * frequency
