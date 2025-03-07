import time
import random
from scapy.all import *

class RandomAccessProcedure:
    def __init__(self, num_ues, num_preambles, contention_free=False):
        self.num_ues = num_ues
        self.num_preambles = num_preambles
        self.contention_free = contention_free
        self.ues = {}  # Stores UE and assigned preamble
        self.gnb_responses = {}  # Stores gNB responses
        self.resolution_results = {}  # Stores Msg4 contention resolution
        self.packets = []  # Stores packets for .pcap file

    def log_packet(self, ue, msg_type, details):
        packet = Ether() / IP(src=f"192.168.1.{ue}", dst="192.168.1.100") / UDP(dport=12345) / Raw(load=f"UE {ue}: {msg_type} - {details}")
        self.packets.append(packet)

    def preamble_selection(self):
        print("\nStep 1: UE selects a PRACH preamble.")
        for ue in range(1, self.num_ues + 1):
            if self.contention_free:
                preamble = ue  # Unique preamble for each UE (CFRA)
            else:
                preamble = random.randint(1, self.num_preambles)  # Random selection (CBRA)
            self.ues[ue] = preamble
            print(f"UE {ue} selected Preamble {preamble}")
            self.log_packet(ue, "Msg1", f"Selected Preamble {preamble}")

    def gnb_response(self):
        print("\nStep 2: gNB sends Random Access Response (RAR) (Msg2).")
        for ue, preamble in self.ues.items():
            if preamble not in self.gnb_responses:
                self.gnb_responses[preamble] = []
            self.gnb_responses[preamble].append(ue)
            print(f"gNB received Preamble {preamble} from UE {ue} - Sending RAR")
            self.log_packet(ue, "Msg2", f"Received RAR for Preamble {preamble}")

    def msg3_transmission(self):
        print("\nStep 3: UE sends RRC Connection Request (Msg3).")
        for preamble, ues in self.gnb_responses.items():
            for ue in ues:
                print(f"UE {ue} sending Msg3 (RRC Request)")
                self.log_packet(ue, "Msg3", "Sent RRC Connection Request")

    def contention_resolution(self):
        print("\nStep 4: gNB resolves contention (Msg4).")
        for preamble, ues in self.gnb_responses.items():
            if len(ues) == 1 or self.contention_free:
                self.resolution_results[ues[0]] = "Success"
                print(f"UE {ues[0]} successfully completes Random Access")
                self.log_packet(ues[0], "Msg4", "Contention Resolution Successful")
            else:
                winner = random.choice(ues)
                self.resolution_results[winner] = "Success"
                print(f"UE {winner} wins contention, others retry")
                self.log_packet(winner, "Msg4", "Won Contention")
                for ue in ues:
                    if ue != winner:
                        self.resolution_results[ue] = "Failure"
                        self.log_packet(ue, "Msg4", "Lost Contention, Retrying")

    def run_simulation(self):
        print("\n---- RANDOM ACCESS SIMULATION STARTED ----")
        self.preamble_selection()
        self.gnb_response()
        self.msg3_transmission()
        self.contention_resolution()
        print("\n---- SIMULATION ENDED ----")
        wrpcap("random_access_simulation.pcap", self.packets)
        print("PCAP file saved as random_access_simulation.pcap")

# Parameters
num_ues = 5  # Number of UEs attempting access
num_preambles = 3  # Number of available preambles

# Run simulation for Contention-Based Random Access (CBRA)
print("\n--- Contention-Based Random Access ---")
cra_sim = RandomAccessProcedure(num_ues, num_preambles, contention_free=False)
cra_sim.run_simulation()

# Run simulation for Contention-Free Random Access (CFRA)
print("\n--- Contention-Free Random Access ---")
cfra_sim = RandomAccessProcedure(num_ues, num_ues, contention_free=True)
cfra_sim.run_simulation()
