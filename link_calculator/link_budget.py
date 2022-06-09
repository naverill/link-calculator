from link_calculator.components.transmitters import Transmitter


class Link:
    def __init__(self, transmit: Transmitter, receive: Transmitter):
        self._transmit = transmit
        self._receive = receive

    @property
    def eb_no(self) -> float:
        pass


class LinkBudget:
    def __init__(self, uplink: Link, downlink: Link):
        self._uplink = uplink
        self._downlink = downlink

    @property
    def eb_no(self) -> float:
        return (self._uplink.eb_no * self._downlink.eb_no) / (
            self._uplink.eb_no + self._downlink.eb_no
        )
