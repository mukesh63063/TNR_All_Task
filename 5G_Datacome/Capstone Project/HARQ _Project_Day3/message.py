import json
import random
import time
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(filename='nas_registration.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Simulate NAS Registration Message with enhanced functionality
class NASMessageGenerator:
    def __init__(self, ue_id: str, imsi: Optional[str] = None, guti: Optional[str] = None):
        self.ue_id = ue_id
        self.imsi = imsi if imsi else self._generate_imsi()
        self.guti = guti if guti else self._generate_guti()
        self.message_type = "Registration Request"
        self.protocol_discriminator = "5GMM"  # 5G Mobility Management
        self.security_header = "Plain NAS"
        self.timestamp = time.ctime()

    def _generate_imsi(self) -> str:
        """Generate a random 15-digit IMSI."""
        return ''.join([str(random.randint(0, 9)) for _ in range(15)])

    def _generate_guti(self) -> str:
        """Generate a random GUTI (simplified format)."""
        return f"GUTI-{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"

    def generate_message(self) -> Dict:
        """Construct the NAS registration message."""
        if len(self.imsi) != 15 or not self.imsi.isdigit():
            raise ValueError(f"Invalid IMSI for {self.ue_id}: {self.imsi}")
        
        nas_message = {
            "UE ID": self.ue_id,
            "Message Type": self.message_type,
            "IMSI": self.imsi,
            "GUTI": self.guti,
            "Protocol Discriminator": self.protocol_discriminator,
            "Security Header Type": self.security_header,
            "Timestamp": self.timestamp,
            "Message ID": random.randint(1000, 9999)  # Unique message identifier
        }
        return nas_message

    def display_message(self) -> None:
        """Display the message and log it."""
        try:
            message = self.generate_message()
            print(f"NAS Registration Message for {self.ue_id}:")
            print(json.dumps(message, indent=4))
            logging.info(f"Generated NAS Message for {self.ue_id}: {json.dumps(message)}")
        except ValueError as e:
            print(f"Error: {e}")
            logging.error(f"Error for {self.ue_id}: {e}")

    def simulate_amf_response(self) -> Dict:
        """Simulate AMF response to the registration request."""
        message = self.generate_message()
        response = {
            "UE ID": self.ue_id,
            "Response Type": "Registration Accept",
            "IMSI": self.imsi,
            "GUTI": self._generate_guti(),  # Assign a new GUTI
            "Cause": "Success",
            "Timestamp": time.ctime()
        }
        print(f"AMF Response for {self.ue_id}:")
        print(json.dumps(response, indent=4))
        logging.info(f"AMF Response for {self.ue_id}: {json.dumps(response)}")
        return response

# Simulate multiple UEs registering
def simulate_nas_registration(num_ues: int = 3):
    print("Simulating NAS Registration for Multiple UEs...")
    for i in range(num_ues):
        ue_id = f"UE{i+1}"
        nas_generator = NASMessageGenerator(ue_id=ue_id)
        nas_generator.display_message()
        time.sleep(1)  # Simulate delay between requests
        nas_generator.simulate_amf_response()
        print("-" * 50)

if __name__ == "__main__":
    simulate_nas_registration(num_ues=2)