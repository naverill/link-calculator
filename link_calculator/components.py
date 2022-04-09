class Antenna:
    def __init__(
        self, name: str, power: float, gain: float, loss: float, frequency: float
    ):
        """
        Instantiate an Antenna object

        Parameters
        ----------
            name (str): Name of antenna
            power (float, W): transmit/receive power of the antenna
            gain (float, W): the power gain of the antenna
            loss (float, W): the power loss of the antenna
            frequency (float, GHz): the transmit frequency of the antenna
        """
        self.power = power
        self.gain = gain
        self.loss = loss
        self.frequency = frequency


class GroundStation:
    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
        antenna: Antenna,
    ):
        """

        Parameters
        ----------
            name (str,): name of the ground station
            latitude (str, deg): the latitude of the groundstation
            longitude (str, deg): the longitude of the groundstation
            altitude (str, km): the altitude of the groundstation above sea level
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.antenna = antenna


class Satellite:
    def __init__(self, name: str, antenna: Antenna):
        self.name = name
        self.antenna = antenna
