from link_calculator.components.modulation import PhaseShiftKeying


def test_energy_per_bit():
    power = 1000  # W
    transmission_rate = 50  # Mbps

    mod_scheme = PhaseShiftKeying(bit_rate=transmission_rate, carrier_power=power)
    print(mod_scheme)
