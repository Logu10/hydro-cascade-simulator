import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from reservoir import ReservoirPlant


def test_reservoir_step():
    config = {
        "name": "Test Plant",
        "head": 50,
        "efficiency": 0.9,
        "max_flow": 200,
        "storage_capacity": 1000,
        "initial_storage": 500
    }
    plant = ReservoirPlant(config)
    outflow = plant.step(100)

    # Check if outflow is within allowable limits
    assert 20 <= outflow <= 200

    # Ensure power and storage history updated
    assert len(plant.history['power_mw']) == 1
    assert plant.storage <= plant.capacity


if __name__ == '__main__':
    test_reservoir_step()
    print("Test passed successfully!")
