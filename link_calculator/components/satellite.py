from link_calculator.components.antennas import Antenna


class Satellite:
    def __init__(self, name: str, antenna: Antenna):
        self.name = name
        self.antenna = antenna
