import random
import json
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid tkinter errors
import matplotlib.pyplot as plt
import socket
from dataclasses import dataclass
from typing import List
import os

@dataclass
class PrachSimulation:
    num_ues: int
    num_preambles: int = 64

    def simulate_cfbra(self) -> dict:
        """Simulate PRACH with CFBRA (Contention-Free)."""
        if self.num_ues <= self.num_preambles:
            success_rate = 1.0
            collision_prob = 0.0
        else:
            successful_ues = self.num_preambles
            success_rate = successful_ues / self.num_ues
            collision_prob = (self.num_ues - self.num_preambles) / self.num_ues

        base_delay = 5.0  # ms
        avg_delay = base_delay + (collision_prob * 10.0)

        return {
            "nUes": self.num_ues,
            "successRate": success_rate,
            "avgDelay": avg_delay,
            "collisionProb": collision_prob,
            "networkStatus": self.check_network()
        }

    def check_network(self) -> str:
        """Check network connectivity."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return "Connected"
        except OSError:
            return "Disconnected"

def run_test_cases(loads: List[int]) -> List[dict]:
    """Run simulations for given UE loads."""
    results = [PrachSimulation(num_ues=load).simulate_cfbra() for load in loads]
    return results

def save_results(results: List[dict], filename: str = "output/prach_results.json"):
    """Save simulation results to a JSON file."""
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    full_path = os.path.join(output_dir, filename)
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure output directory exists
        with open(full_path, "w") as f:
            json.dump(results, f, indent=4)
    except Exception as e:
        print(f"Error saving results: {e}")
        raise

def generate_graphical_report(results: List[dict]):
    """Generate graphs and save as PNG in the output folder."""
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    full_path = os.path.join(output_dir, "prach_graph.png")
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure output directory exists
        loads = [r["nUes"] for r in results]
        success_rates = [r["successRate"] * 100 for r in results]
        delays = [r["avgDelay"] for r in results]

        plt.figure(figsize=(10, 6))
        plt.plot(loads, success_rates, label="Success Rate (%)", marker="o")
        plt.plot(loads, delays, label="Avg Delay (ms)", marker="x")
        plt.xlabel("Number of UEs")
        plt.ylabel("Metrics")
        plt.title("PRACH Performance with CFBRA")
        plt.legend()
        plt.grid(True)
        plt.savefig(full_path)
    except Exception as e:
        print(f"Error saving graph: {e}")
        raise
    plt.close()