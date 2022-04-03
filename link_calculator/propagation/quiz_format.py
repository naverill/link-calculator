from link_calculator.constants import EARTH_RADIUS
from link_calculator.propagation.conversions import decibel_to_watt, watt_to_decibel, frequency_to_wavelength
from link_calculator.propagation.utils import (
    receive_power 
)


def test_receive_power(
    transmit_power: float,
    transmit_loss: float,
    transmit_gain: float,
    distance: float,
    receive_gain: float,
    receive_loss: float,
    atmospheric_loss: float,
    wavelength: float = None,
    eff_aperture: float = None
) -> None:
    power = receive_power(
        transmit_power,
        transmit_loss,
        transmit_gain,
        distance,
        receive_loss,
        receive_gain,
        atmospheric_loss,
        wavelength,
        eff_aperture, 
    )
    print("Receive Power (dBW): ", watt_to_decibel(power))



if __name__ == "__main__":
    trans_power = 9 # W
    trans_gain = decibel_to_watt(16) # W
    trans_loss = decibel_to_watt(-3)  # W
    print(trans_loss)
    distance = 24500 * 1000 # m
    
    receive_loss = decibel_to_watt(-2) # W
    receive_gain = decibel_to_watt(57) # W
    
    atmospheric_loss = decibel_to_watt(-9) # W

    eff_aperture = None # m^2
    wavelength = frequency_to_wavelength(11) # m 

    test_receive_power(
      trans_power,
      trans_loss,
      trans_gain,
      distance,
      receive_loss,
      receive_gain,
      atmospheric_loss,
      wavelength=wavelength 
    )

    

