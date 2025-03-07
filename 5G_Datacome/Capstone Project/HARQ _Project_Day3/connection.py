import random
import time
import logging
from enum import Enum
from typing import Optional

# Configure logging
logging.basicConfig(filename='rrc_connection.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Define RRC States
class RRCState(Enum):
    IDLE = "IDLE"
    CONNECTED = "CONNECTED"
    FAILED = "FAILED"

# Simulate RRC Connection Process
class RRCStateMachine:
    def __init__(self, ue_id: str, signal_strength: Optional[float] = None):
        self.ue_id = ue_id
        self.current_state = RRCState.IDLE
        self.signal_strength = signal_strength if signal_strength is not None else random.uniform(0, 100)  # 0-100 dBm
        self.min_signal_threshold = 30.0  # Minimum signal strength for connection
        self.attempts = 0
        self.max_attempts = 3

    def initiate_connection(self) -> bool:
        """Attempt to establish an RRC connection."""
        print(f"UE {self.ue_id}: Current State = {self.current_state.value}, Signal Strength = {self.signal_strength:.2f} dBm")
        logging.info(f"UE {self.ue_id} Attempting Connection - State: {self.current_state.value}, Signal: {self.signal_strength:.2f}")

        if self.current_state != RRCState.IDLE:
            print(f"UE {self.ue_id}: Cannot initiate connection from {self.current_state.value} state")
            return False

        self.attempts += 1
        if self.signal_strength < self.min_signal_threshold:
            print(f"UE {self.ue_id}: Signal strength too low ({self.signal_strength:.2f} < {self.min_signal_threshold})")
            self.current_state = RRCState.FAILED
            logging.warning(f"UE {self.ue_id} Failed - Low Signal")
            return False

        if self.attempts > self.max_attempts:
            print(f"UE {self.ue_id}: Max connection attempts ({self.max_attempts}) exceeded")
            self.current_state = RRCState.FAILED
            logging.error(f"UE {self.ue_id} Failed - Max Attempts Exceeded")
            return False

        print(f"UE {self.ue_id}: Sending RRC Connection Request (Attempt {self.attempts})...")
        time.sleep(1)  # Simulate signaling delay
        print(f"UE {self.ue_id}: Received RRC Connection Setup...")
        self.current_state = RRCState.CONNECTED
        print(f"UE {self.ue_id}: State transitioned to {self.current_state.value}")
        logging.info(f"UE {self.ue_id} Connected Successfully")
        return True

    def release_connection(self) -> None:
        """Release the RRC connection."""
        if self.current_state == RRCState.CONNECTED:
            print(f"UE {self.ue_id}: Sending RRC Connection Release Request...")
            time.sleep(0.5)
            self.current_state = RRCState.IDLE
            print(f"UE {self.ue_id}: Connection released, State = {self.current_state.value}")
            logging.info(f"UE {self.ue_id} Connection Released")
        else:
            print(f"UE {self.ue_id}: No active connection to release")

    def display_state(self) -> None:
        """Display the current state."""
        print(f"UE {self.ue_id}: Current RRC State = {self.current_state.value}")

# Simulate RRC connection for multiple UEs
def simulate_rrc_connection(num_ues: int = 3):
    print("Simulating RRC Connection Establishment...")
    ues = [RRCStateMachine(ue_id=f"UE{i+1}") for i in range(num_ues)]
    
    for ue in ues:
        ue.display_state()
        success = ue.initiate_connection()
        if success:
            time.sleep(1)
            ue.release_connection()
        ue.display_state()
        print("-" * 50)

if __name__ == "__main__":
    simulate_rrc_connection(num_ues=3)