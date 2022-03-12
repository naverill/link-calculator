from math import radians, cos, acos, sin, sqrt, pi, atan, tan


from constants import EARTH_RADIUS,EARTH_MU


def calc_velocity(semi_major_axis: float, orbital_radius: float, mu: float = EARTH_MU) -> float:
	"""
	Calculate the velocity of a satellite in orbit according to Kepler's second law 

	Parameters
	---------
		semi_major_axis (float, km): The semi-major axis of the orbit 
		orbital_radius (float, km): distance from the centre of mass to the satellite
		mu (float, optional): Kepler's gravitational constant 	

	Returns
	------
		velocity (float, km/s): the orbit speed of the satellite 
	"""
	return sqrt(mu * (2 / r - 1 / a))


def calc_velocity_circular(orbital_radius: float, mu: float = EARTH_MU) -> float:
	"""
	Special case of calc_velocity where r = a	

	Parameters
	---------
		orbital_radius (float, km): distance from the centre of mass to the satellite
		mu (float, optional): Kepler's gravitational constant 	

	Returns
	------
		velocity (float, km/s): the orbit speed of the satellite 
	"""
	return calc_velocity(r, r, mu)



def calc_period(semi_major_axis: float, mu: float = EARTH_MU) -> float:
	"""
	Calculate the period of the satellite's orbit according to Kepler's third law	

	Parameters
	---------
		semi_major_axis (float, km): The semi-major axis of the orbit 
		mu (float, optional): Kepler's gravitational constant 	

	Returns
	------
		period (float, s): the time taken for the satellite to complete a revolution 
	"""
	return 2 * pi * sqrt(semi_major_axis**3 / mu)


def calc_angle_sat_to_ground_station(ground_station_lat: float, ground_station_long: float, sat_lat: float, sat_long: float) -> float:
	"""
	Calculate angle gamma at the centre of the ground, between the Earth station and the satellite

	Parameters
	---------
		ground_station_lat (float, deg): the latitude of the ground station
		ground_station_long (float, deg): the longitude of the ground station
		sat_lat (float, deg): the latitude of the satellite
		sat_long (float, deg): the longitude of the satellite 

	Returns
	------
		gamma (float, rad): angle between satellite and ground station
	"""
	gs_lat_rad = radians(ground_station_lat)
	gs_long_rad = radians(ground_station_long)
	sat_lat_rad = radians(sat_lat)
	sat_long_rad = radians(sat_long)

	return acos(
		cos(gs_lat_rad) * cos(sat_lat_rad) * cos(sat_long_rad - gs_long_rad) + sin(gs_lat_rad) * sin(sat_lat_rad)
	)


def calc_slant_range(orbital_radius: float, angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS) -> float:
	"""
	Calculate the slant range from the ground station to the satellite

	Parameters
	----------
		orbital_radius (float, km): distance from the centre of mass to the satellite
		angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass
		planet_radius (float, km, optional): radius of the planet

	Return
	------
		slant_range (float, km): the distance from the ground station to the satellite

	"""
	return sqrt(planet_radius ** 2 + orbital_radius ** 2 - 2 * planet_radius * orbital_radius * cos(angle_sat_to_gs))


def calc_elevation_angle(orbital_radius: float, angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS) -> float:
	"""
	Calculate the elevation angle from the ground station to the satellite

	Parameters
	----------
		orbital_radius (float, km): distance from the centre of mass to the satellite
		angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass
		planet_radius (float, km, optional): radius of the planet

	Return
	------
		elevation_angle (float, rad): the distance from the ground station to the satellite

	"""
	return acos(
		sin(angle_sat_to_gs) / (1 + (planet_radius / orbital_radius) ** 2 - 2 * (planet_radius / orbital_radius) * cos(angle_sat_to_gs))
	)




def calc_area_of_coverage(angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS):
	"""
	Calculate the surface area coverage of the Earth from a satellite 

	Parameters
	----------
		angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass
		planet_radius (float, km, optional): radius of the planet

	Return
	------
		area_coverage (float, km): the area of the Earth's surface visible from a satellite  

	"""
	return 2 * pi * planet_radius ** 2 (1 - cos(angle_sat_to_gs)) 


def calc_percentage_of_coverage(angle_sat_to_gs: float, planet_radius: float = EARTH_RADIUS) -> float:
	"""
	Calculate the surface area coverage of the Earth from a satellite as a percentage of the total
		surface area  

	Parameters
	----------
		angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass
		planet_radius (float, km, optional): radius of the planet

	Return
	------
		area_coverage (float, %): the percentage of the Earth's surface visible from a satellite  

	"""
	return area_of_coverage(angle_sat_to_gs, planet_radius) / (4 * pi * planet_radius ** 2) * 100

	
def calc_percentage_of_coverage_gamma(angle_sat_to_gs: float) -> float:
	"""
	Calculate the surface area coverage of the Earth from a satellite as a percentage of the total
		surface area  

	Parameters
	----------
		angle_sat_to_gs (float, rad): angle from the satellite to the ground station, centred at the centre of mass

	Return
	------
		area_coverage (float, %): the percentage of the Earth's surface visible from a satellite  

	"""
	return 50 * (1 - cos(angle_sat_to_gs)) 


def calc_azimuth_intermediate(ground_station_lat: float, ground_station_long: float, sat_long: float) -> float:
	"""
	Calculate the azimuth of a geostationary satellite 

	Parameters
	---------
		ground_station_lat (float, deg): the latitude of the ground station
		ground_station_long (float, deg): the longitude of the ground station
		sat_long (float, deg): the longitude of the satellite 

	Returns
	------
		azimuth (float, rad): horizontal pointing angle of the ground station antenna to 
			the satellite. The azimuth angle is usually measured in clockwise direction 
			in degrees from true north. 
	"""
	gs_lat_rad = radians(ground_station_lat)
	gs_long_rad = radians(ground_station_long)
	sat_long_rad = radians(sat_long)
	return atan(
		tan(abs(sat_long_rad - gs_long_rad)) / sin(gs_lat_rad)
	)


def calc_percentage_of_coverage_height(orbital_radius: float, min_angle: float = 0.0, planet_radius: float = EARTH_RADIUS) -> float:
	return calc_max_visible_distance(orbital_radius, 0, min_angle, planet_radius) / (4 * pi * planet_radius ** 2)

def calc_max_visible_distance(orbital_radius: float, ground_station_lat: float, min_angle: float = 0.0, planet_radius: float = EARTH_RADIUS) -> float:
	"""
	Calculate the radius of visibility for a satellite and a ground station 

	Parameters
	---------
		orbital_radius (float, km): the radius of the satellite from the centre of the Earth 
		ground_station_lat (float, deg): the latitude of the ground station
		min_angle (float, deg): the minimum angle of visibility over the horizon 
		planet_radius (float, km, optional): radius of the planet

	Returns
	------
		azimuth (float, rad): horizontal pointing angle of the ground station antenna to 
			the satellite. The azimuth angle is usually measured in clockwise direction 
			in degrees from true north. 
	"""
	gs_lat_rad = radians(ground_station_lat)
	min_angle_rad = radians(min_angle)
	return acos(
		cos(
			(acos((planet_radius / orbital_radius) * cos(min_angle_rad)) - min_angle_rad) / cos(gs_lat_rad)
		)
	)



def calc_azimuth(ground_station_lat: float, ground_station_long: float, sat_lat: float, sat_long: float) -> float:
	"""
	Calculate the azimuth of a satellite 

	Parameters
	---------
		ground_station_lat (float, deg): the latitude of the ground station
		ground_station_long (float, deg): the longitude of the ground station
		sat_lat (float, deg): the latitude of the satellite 
		sat_long (float, deg): the longitude of the satellite 

	Returns
	------
		azimuth (float, rad): horizontal pointing angle of the ground station antenna to 
			the satellite. The azimuth angle is usually measured in clockwise direction 
			in degrees from true north. 
	"""
#	# Ground station is in northern hemisphere
#	if 90 > gs_long_rad > 0:	
#
	# At the equator
#	elif gs_long_rad == 0:
#		return azimuth_geo(ground_station_lat, ground_station_long, sat_long)
#	# In the southern hemisphere
#	elif 0 > gs_long_rad >= 90:
#		if (sat_lat - ground_station_lat)
#		return pi / 2
#	else:
#		raise ValueError("Invalid value for the ground station's longitude: must be in range -90 < L < 90")
	return NotImplementedError
