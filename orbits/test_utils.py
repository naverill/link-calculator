from math import isclose, radians

from utils import * 

def test_period():
	height = [250, 500, 1000, 1000]
	period = [5400, 5677, 6307, 20860]

	for h, T in zip(height, period):
		assert isclose(calc_period(h), T)

def test_percentage_of_coverage():
	height = [250, 500, 1000, 10000, 10000]
	angle = [0, 0, 0, 0, 5]
	per = [1.89, 3.63, 6.78, 30.53, 26.66]

	for h, a, p in zip(height, angle, per):
		assert isclose(calc_percentage_of_coverage_height(h, a), p)

	
def test_azimuth_intermediate():
	gs_lat = 30
	gs_long = 120
	sat_lat = 90
	sat_long = 0
	orbital_radius = 42164

	assert isclose(calc_azimuth_intermediate(gs_lat, gs_long, sat_long), radians(49.11))


def test_azimuth_intermediate_2():
	gs_lat = 30
	gs_long = 30
	sat_lat = 30
	
	sat_long = 0
	orbital_radius = 42164

	
	assert isclose(calc_azimuth_intermediate(gs_lat, gs_long, sat_long), radians(73.9))


def test_elevation_angle():
	gs_lat = 30
	gs_long = 120
	sat_lat = 90

	# Geo-stationary satellite
	sat_long = 0
	orbital_radius = 42164

	gamma = calc_angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)

	assert isclose(calc_elevation_angle(orbital_radius, gamma), radians(42.15))


def test_elevation_angle_2():
	gs_lat = 30
	gs_long = 30
	sat_lat = 30
	
	sat_long = 0
	orbital_radius = 42164


	gamma = calc_angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)

	assert isclose(calc_elevation_angle(orbital_radius, gamma), radians(42.15))


def test_slant_angle():
	gs_lat = 30
	gs_long = 120
	sat_lat = 90

	# Geo-stationary satellite
	sat_long = 0
	orbital_radius = 42164

	gamma = calc_angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
	assert isclose(calc_slant_range(orbital_radius, gamma), 37618)
	


def test_slant_angle_2():
	gs_lat = 30
	gs_long = 30
	sat_lat = 30
	
	sat_long = 0
	orbital_radius = 42164


	gamma = calc_angle_sat_to_ground_station(gs_lat, gs_long, sat_lat, sat_long)
	assert isclose(calc_slant_range(orbital_radius, gamma), 39819)

	
