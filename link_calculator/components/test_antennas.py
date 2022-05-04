import numpy as np

from link_calculator.components.antennas import ParabolicAntenna


def test_parabolic_antenna():
    efficiency_ = [1, 0.6]
    gain_ = [62.41, 60.19]

    for e, g in zip(efficiency_, gain_):
        ant = ParabolicAntenna(
            name="test", circular_diameter=9, efficiency=e, frequency=14
        )
        assert np.isclose(ant.gain, g)
