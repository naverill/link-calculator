from link_calulator.orbits.utils import slant_range

from link_calculator.components.communicators import Communicator
from link_calculator.constants import BOLTZMANN_CONSTANT
from link_calculator.propagation.utils import free_space_loss


class LinkBudget:
    def __init__(
        self,
        satellite: Communicator,
        ground_station: Communicator,
        atmospheric_loss: float = 1,
        min_elevation: float = 0,
    ):
        self._sat = satellite
        self._gs = ground_station
        self._min_elevation = min_elevation
        self.atmospheric_loss = atmospheric_loss

    @property
    def distance(self) -> float:
        gamma = self.ground_station.coordinate.central_angle(
            self.satellite.sub_satellite_point
        )
        return slant_range(self.satellite.orbit.orbital_radius, gamma)

    @property
    def satellite_carrier_power(self) -> float:
        if self._sat_carrier_power is None:
            self._sat_carrier_power = (
                self.ground_station.transmit.eirp
                * free_space_loss(
                    self.distance, self.ground_station.transmit.wavelength
                )
                * self.atmospheric_loss
            )
        return self._sat_carrier_power

    @property
    def uplink_carrier_to_noise(self) -> float:
        if self._uplink_carrier_to_noise is None:
            self._uplink_carrier_to_noise = (
                self.satellite.combined_gain * self.satellite_carrier_power
            ) / (BOLTZMANN_CONSTANT * self.satellite.equiv_noise_temp)
        return self._uplink_carrier_to_noise

    @property
    def uplink_eb_no(self) -> float:
        if self._uplink_eb_no is None:
            self._uplink_eb_no = (
                self.uplink_carrier_to_noise
                * self.ground_station.transmit.modulation.bit_rate
            )

    @property
    def downlink_carrier_to_noise(self) -> float:
        if self._downlink_carrier_to_noise is None:
            self._downlink_carrier_to_noise = (
                self.ground_station.combined_gain * self.ground_station_carrier_power
            ) / (BOLTZMANN_CONSTANT * self.ground_station.equiv_noise_temp)
        return self._downlink_carrier_to_noise

    @property
    def downlink_eb_no(self) -> float:
        if self._downlink_eb_no is None:
            self._downlink_eb_no = (
                self.downlink_carrier_to_noise
                * self.satellite.transmit.modulation.bit_rate
            )
        return self._downlink_eb_no

    @property
    def ground_station_carrier_power(self, distance) -> float:
        if self._gs_carrier_power is None:
            self._gs_carrier_power = (
                self.satellite.transmit.eirp
                * free_space_loss(self.distance, self.satellite.transmit.wavelength)
                * self.atmospheric_loss
            )
        return self._gs_carrier_power

    @property
    def eb_no(self) -> float:
        return (self.uplink_eb_no * self.downlink_eb_no) / (
            self.uplink_eb_no + self._downlink_eb_no
        )

    @property
    def satellite(self) -> Communicator:
        return self._sat

    @property
    def ground_station(self) -> Communicator:
        return self._gs
