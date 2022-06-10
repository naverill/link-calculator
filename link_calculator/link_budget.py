from link_calulator.orbits.utils import slant_range

from link_calculator.components.communicators import Communicator
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
        return (self._uplink.eb_no * self._downlink.eb_no) / (
            self._uplink.eb_no + self._downlink.eb_no
        )

    @property
    def satellite(self) -> Communicator:
        return self._sat

    @property
    def ground_station(self) -> Communicator:
        return self._gs
