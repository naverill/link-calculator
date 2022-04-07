class Antenna:
    def __init__(self, name: str, power: float, gain: float, loss: float):
        self.power = power
        self.gain = gain
        self.loss = loss


class GroundStation:
    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
        antenna: Antenna,
    ):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.antenna = antenna


class Satellite:
    def __init__(self, name: str, antenna: Antenna):
        self.name = name
        self.antenna = antenna
