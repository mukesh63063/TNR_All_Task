import sys
sys.path.append('..')  # Add parent directory to path

from prach_simulation import PrachSimulation  # Use relative import

def test_low_load_success():
    sim = PrachSimulation(num_ues=10)
    result = sim.simulate_cfbra()
    assert result["successRate"] == 1.0, "Low load should have 100% success"
    assert result["collisionProb"] == 0.0, "No collisions expected"

def test_high_load_collision():
    sim = PrachSimulation(num_ues=100)
    result = sim.simulate_cfbra()
    assert result["successRate"] < 1.0, "High load should have reduced success"
    assert result["collisionProb"] > 0.0, "Collisions expected"

def test_network_check():
    sim = PrachSimulation(num_ues=10)
    result = sim.simulate_cfbra()
    assert result["networkStatus"] in ["Connected", "Disconnected"]