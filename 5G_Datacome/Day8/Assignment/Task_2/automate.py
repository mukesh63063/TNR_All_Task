import random
import time
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CompressorClass:
    """Handles ROHC header compression for 5G NR packets."""
    def __init__(self):
        self.compressed_data = []
        self.compression_errors = 0
    
    def compress_packet(self, packet, compression_rate=0.8):
        try:
            if random.random() < 0.95:  # 95% success rate
                compressed_size = len(packet) * (1 - compression_rate)
                compressed_packet = f"Compressed_{packet}_Size_{compressed_size:.2f}"
                self.compressed_data.append(compressed_packet)
                return compressed_packet, compressed_size
            else:
                self.compression_errors += 1
                raise ValueError("Compression failed due to network error")
        except Exception as e:
            logging.error(f"Compression error: {str(e)}")
            return None, 0

class DecompressorClass:
    """Handles ROHC header decompression for 5G NR packets."""
    def __init__(self):
        self.decompressed_data = []
        self.decompression_errors = 0
    
    def decompress_packet(self, compressed_packet, success_rate=0.95):
        try:
            if random.random() < success_rate:
                decompressed_packet = f"Decompressed_{compressed_packet}"
                self.decompressed_data.append(decompressed_packet)
                return decompressed_packet
            else:
                self.decompression_errors += 1
                logging.warning("Decompression failed due to channel noise")
                return None
        except Exception as e:
            logging.error(f"Decompression error: {str(e)}")
            return None

class ProfileManager:
    """Manages ROHC profiles for compression/decompression settings."""
    def __init__(self):
        self.profiles = {}
    
    def manage_profile(self, profile_id, settings):
        self.profiles[profile_id] = settings
        return f"Profile {profile_id} configured with {settings}"

class GNBNodeModel:
    """Simulates a 5G NR gNB (base station) node."""
    def __init__(self):
        self.connected_ues = []
        self.signal_strength = random.uniform(70, 100)  # dBm
    
    def connect_ue(self, ue):
        if random.random() < 0.98:  # 98% connection success
            self.connected_ues.append(ue)
            return f"gNB connected to UE: {ue} with signal strength {self.signal_strength:.2f} dBm"
        return "Connection failed due to interference"

class UENodeModel:
    """Simulates a 5G NR UE (user equipment) node."""
    def __init__(self, ue_id):
        self.ue_id = ue_id
        self.connection_status = "Disconnected"
        self.battery_level = random.uniform(80, 100)  # Percentage
    
    def connect_to_gnb(self, gnb):
        if random.random() < 0.98:
            self.connection_status = "Connected"
            return f"UE {self.ue_id} connected to gNB: {gnb} with battery {self.battery_level:.2f}%"
        return f"UE {self.ue_id} connection failed due to UE issues"

class ChannelModel:
    """Simulates the 5G NR communication channel."""
    def __init__(self):
        self.channel_conditions = "Normal"
        self.packet_loss_rate = random.uniform(0.01, 0.05)  # 1-5% packet loss
    
    def simulate_channel(self):
        if random.random() < self.packet_loss_rate:
            return f"Channel condition: Poor (Packet loss detected at {self.packet_loss_rate*100:.2f}%)"
        return f"Channel condition: {self.channel_conditions} (Loss rate: {self.packet_loss_rate*100:.2f}%)"

class PacketGenerator:
    """Generates test packets for simulation."""
    def __init__(self):
        self.packets = []
        self.packet_size = random.uniform(100, 1000)  # Bytes
    
    def generate_packet(self, packet_type):
        packet = f"Packet_{packet_type}_Size_{self.packet_size:.2f}B"
        self.packets.append(packet)
        return packet, self.packet_size

class TrafficModels:
    """Simulates network traffic patterns."""
    def __init__(self):
        self.traffic_patterns = []
        self.traffic_volume = random.uniform(1000, 5000)  # KB/s
    
    def generate_traffic(self, pattern):
        traffic = f"Traffic_{pattern}_Volume_{self.traffic_volume:.2f}KB/s"
        self.traffic_patterns.append(traffic)
        return traffic

class MetricsCollector:
    """Collects performance metrics during simulation."""
    def __init__(self):
        self.metrics = {}
    
    def collect_metric(self, metric_name, value):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.metrics[metric_name] = {"value": value, "timestamp": timestamp}
        logging.info(f"Metric collected: {metric_name} = {value} at {timestamp}")
        return value

class AnalysisTools:
    """Analyzes simulation data for insights."""
    def analyze_data(self, data):
        return f"Analysis result for {data}: Processed successfully"

class ResultsVisualization:
    """Visualizes simulation results using matplotlib with bar, line, and scatter plots."""
    def visualize_results(self, metrics, packet_size=None, output_dir="output"):
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            metric_names = list(metrics.keys())
            metric_values = {}
            for m in metric_names:
                value_str = str(metrics[m]["value"])
                if "ms" in value_str:
                    metric_values[m] = float(value_str.replace("ms", "").strip())
                elif "Mbps" in value_str:
                    metric_values[m] = float(value_str.replace("Mbps", "").strip())
                else:
                    metric_values[m] = float(value_str)

            # Bar Plot: Overview of All Metrics
            if metric_values:
                plt.figure(figsize=(10, 6))
                plt.bar(metric_names, metric_values.values(), color='skyblue')
                plt.title("5G NR ROHC Simulation Metrics Overview")
                plt.xlabel("Metric Type")
                plt.ylabel("Value")
                plt.grid(True)
                bar_file = os.path.join(output_dir, "metrics_bar.png")
                plt.savefig(bar_file, bbox_inches='tight')
                plt.close()
                logging.info(f"Bar plot saved to {bar_file}")
            else:
                bar_file = "Bar plot not generated (no metrics available)"
                logging.warning("Bar plot skipped: No metrics available")

            # Simulate multiple data points for line and scatter plots
            num_points = 5

            # Line Plot: Latency over Time
            if "Latency" in metric_values:
                latency_base = metric_values["Latency"]
                latencies = [latency_base * random.uniform(0.9, 1.1) for _ in range(num_points)]
                time_points = [i for i in range(num_points)]  # Simplified time axis
                plt.figure(figsize=(10, 6))
                plt.plot(time_points, latencies, marker='o', color='blue', linestyle='-')
                plt.title("Latency Over Time in 5G NR ROHC Simulation")
                plt.xlabel("Time (simulated steps)")
                plt.ylabel("Latency (ms)")
                plt.grid(True)
                line_file = os.path.join(output_dir, "latency_line.png")
                plt.savefig(line_file, bbox_inches='tight')
                plt.close()
                logging.info(f"Line plot saved to {line_file}")
            else:
                line_file = "Line plot not generated (no Latency data)"
                logging.warning("Line plot skipped: No Latency metric available")

            # Scatter Plot: Throughput vs. Packet Size
            if "Throughput" in metric_values and packet_size is not None:
                throughput_base = metric_values["Throughput"]
                throughputs = [throughput_base * random.uniform(0.9, 1.1) for _ in range(num_points)]
                packet_sizes = [packet_size * random.uniform(0.8, 1.2) for _ in range(num_points)]
                plt.figure(figsize=(10, 6))
                plt.scatter(packet_sizes, throughputs, color='red', label='Throughput vs Packet Size')
                plt.title("Throughput vs. Packet Size in 5G NR ROHC Simulation")
                plt.xlabel("Packet Size (Bytes)")
                plt.ylabel("Throughput (Mbps)")
                plt.grid(True)
                plt.legend()
                scatter_file = os.path.join(output_dir, "throughput_scatter.png")
                plt.savefig(scatter_file, bbox_inches='tight')
                plt.close()
                logging.info(f"Scatter plot saved to {scatter_file}")
            else:
                scatter_file = "Scatter plot not generated (no Throughput or packet_size)"
                logging.warning("Scatter plot skipped: Missing Throughput or packet_size")

            return f"Visualizations saved to '{output_dir}' (Bar: {bar_file}, Line: {line_file}, Scatter: {scatter_file})"
        except Exception as e:
            logging.error(f"Visualization error: {str(e)}")
            return f"Failed to generate visualizations: {str(e)}"

class RandomAccessModule:
    """Simulates 3GPP-compliant random access with contention resolution (TS 38.321)."""
    def __init__(self, num_ues=5, preamble_count=64, max_attempts=10, backoff_window=20):
        self.num_ues = num_ues
        self.preamble_count = preamble_count  # Total preambles available (3GPP TS 38.211)
        self.max_attempts = max_attempts  # Max RA attempts per UE (3GPP configurable)
        self.backoff_window = backoff_window  # Backoff window in ms (3GPP TS 38.321)
        self.successful_accesses = 0
        self.collisions = 0
        self.access_delays = []
        self.contention_events = []

    def perform_random_access(self, gnb, channel):
        """Simulate 3GPP contention-based random access (CBRA) with collision avoidance."""
        successful_accesses = 0
        collisions = 0
        access_delays = []
        preamble_usage = {}  # Tracks preamble assignments to detect collisions
        
        for ue_id in range(1, self.num_ues + 1):
            attempt = 0
            success = False
            delay = 0
            
            while attempt < self.max_attempts and not success:
                attempt += 1
                preamble = random.randint(0, self.preamble_count - 1)
                initial_delay = random.uniform(5, 10)  # Initial RA delay in ms
                delay += initial_delay
                
                if preamble in preamble_usage:
                    collisions += 1
                    self.contention_events.append(f"UE {ue_id} collided on preamble {preamble}, attempt {attempt}")
                    logging.warning(f"Collision: UE {ue_id} on preamble {preamble}")
                    
                    backoff = random.uniform(0, self.backoff_window)
                    delay += backoff
                    time.sleep(backoff / 1000)  # Simulate backoff delay
                    continue
                
                if random.random() < (1 - channel.packet_loss_rate):
                    preamble_usage[preamble] = ue_id  # Reserve preamble
                    
                    if random.random() < 0.95:  # 95% success for Msg4 (contention resolution)
                        successful_accesses += 1
                        success = True
                        access_delays.append(delay)
                        self.contention_events.append(f"UE {ue_id} succeeded on preamble {preamble}, delay {delay:.2f}ms")
                        logging.info(f"UE {ue_id} RA success: preamble {preamble}, delay {delay:.2f}ms")
                    else:
                        logging.warning(f"UE {ue_id} RA failed at Msg4, preamble {preamble}")
                else:
                    logging.warning(f"UE {ue_id} RA failed due to channel loss, preamble {preamble}")
                
                time.sleep(initial_delay / 1000)  # Simulate processing delay
            
            if not success:
                self.contention_events.append(f"UE {ue_id} exhausted {self.max_attempts} attempts")
        
        self.successful_accesses += successful_accesses
        self.collisions += collisions
        self.access_delays.extend(access_delays)
        
        avg_delay = sum(access_delays) / len(access_delays) if access_delays else 0
        return {
            "successful_accesses": successful_accesses,
            "collisions": collisions,
            "average_access_delay": avg_delay
        }

class ScenarioGenerator:
    """Generates test scenarios for simulation."""
    def __init__(self):
        self.scenarios = []
    
    def generate_scenario(self, description):
        complexity = random.uniform(1, 5)
        scenario = f"Scenario_{description}_Complexity_{complexity:.2f}"
        self.scenarios.append(scenario)
        return scenario

class TestExecutionEngine:
    """Executes test scenarios with error handling."""
    def execute_test(self, scenario, packet):
        delay = random.uniform(0.1, 1.0)
        time.sleep(delay)
        if random.random() < 0.95:
            return f"Test executed for {scenario} with {packet} (Delay: {delay:.2f}s)"
        return f"Test failed for {scenario} due to timeout"

class PerformanceMonitor:
    """Monitors performance metrics in real-time."""
    def monitor_performance(self, metric):
        value_str = metric
        if "ms" in value_str:
            value = float(value_str.replace("ms", "").strip()) * random.uniform(0.9, 1.1)
            unit = "ms"
        elif "Mbps" in value_str:
            value = float(value_str.replace("Mbps", "").strip()) * random.uniform(0.9, 1.1)
            unit = "Mbps"
        else:
            value = float(value_str) * random.uniform(0.9, 1.1)
            unit = ""
        return f"Monitoring performance: {value:.2f}{unit}"

class ReportGenerator:
    """Generates a detailed report of the simulation."""
    def __init__(self):
        self.reports = []
    
    def generate_detailed_report(self, events, metrics, ra_metrics, output_file="output/simulation_report.txt"):
        try:
            report = ["=== 5G NR ROHC Simulation Report ===\n"]
            report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.append("Simulation Events:\n")
            for event in events:
                report.append(f"- {event}\n")
            report.append("\nPerformance Metrics:\n")
            for metric_name, data in metrics.items():
                report.append(f"{metric_name}: {data['value']} (at {data['timestamp']})\n")
            report.append("\nRandom Access Metrics:\n")
            report.append(f"Successful Accesses: {ra_metrics['successful_accesses']}\n")
            report.append(f"Collisions: {ra_metrics['collisions']}\n")
            report.append(f"Average Access Delay: {ra_metrics['average_access_delay']:.2f}ms\n")
            
            report_text = "".join(report)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding='utf-8') as f:
                f.write(report_text)
            logging.info(f"Report saved to {output_file}")
            return report_text
        except Exception as e:
            logging.error(f"Report generation error: {str(e)}")
            return f"Failed to generate report: {str(e)}"

class ConfigurationManagement:
    """Manages system configurations."""
    def __init__(self):
        self.configs = {}
    
    def configure_system(self, component, settings):
        if not isinstance(settings, dict):
            raise ValueError("Settings must be a dictionary")
        self.configs[component] = settings
        return f"Configured {component} with {settings}"

class ROHCModule:
    """Manages ROHC compression and decompression components."""
    def __init__(self):
        self.compressor = CompressorClass()
        self.decompressor = DecompressorClass()
        self.profile_manager = ProfileManager()

class FiveGNRIntegration:
    """Integrates 5G NR components for simulation."""
    def __init__(self):
        self.gnb = GNBNodeModel()
        self.ue = UENodeModel("UE_1")
        self.channel = ChannelModel()

class TestFramework:
    """Handles testing and analysis components."""
    def __init__(self):
        self.packet_generator = PacketGenerator()
        self.traffic_models = TrafficModels()
        self.metrics_collector = MetricsCollector()
        self.analysis_tools = AnalysisTools()
        self.results_visualization = ResultsVisualization()

class AutomationFramework:
    """Automates simulation testing and reporting."""
    def __init__(self):
        self.scenario_generator = ScenarioGenerator()
        self.test_execution_engine = TestExecutionEngine()
        self.performance_monitor = PerformanceMonitor()
        self.report_generator = ReportGenerator()

class NS342ROHCSimulation:
    """Orchestrates the 5G NR ROHC simulation."""
    def __init__(self):
        self.rohc_module = ROHCModule()
        self.fiveg_nr = FiveGNRIntegration()
        self.test_framework = TestFramework()
        self.automation_framework = AutomationFramework()
        self.config_manager = ConfigurationManagement()
        self.random_access = RandomAccessModule(num_ues=5, preamble_count=64, max_attempts=10, backoff_window=20)

    def run_simulation(self):
        simulation_events = []
        packet_size = None
        
        try:
            config_result = self.config_manager.configure_system("ROHC_Module", {"compression_level": "high", "profile": "UDP/IP"})
            simulation_events.append(f"System configuration: {config_result}")
            
            gnb_connection = self.fiveg_nr.gnb.connect_ue("UE_1")
            ue_connection = self.fiveg_nr.ue.connect_to_gnb("gNB_1")
            channel_status = self.fiveg_nr.channel.simulate_channel()
            simulation_events.append(f"5G NR connection: {gnb_connection}")
            simulation_events.append(f"UE connection: {ue_connection}")
            simulation_events.append(f"Channel status: {channel_status}")
            
            ra_metrics = self.random_access.perform_random_access(self.fiveg_nr.gnb, self.fiveg_nr.channel)
            simulation_events.append(f"Random access: {ra_metrics['successful_accesses']} successes, {ra_metrics['collisions']} collisions, avg delay {ra_metrics['average_access_delay']:.2f}ms")
            
            traffic = self.test_framework.traffic_models.generate_traffic("High_Load")
            packet, packet_size = self.test_framework.packet_generator.generate_packet("Data")
            simulation_events.append(f"Generated traffic: {traffic}")
            simulation_events.append(f"Generated packet: {packet}")
            
            compressed_packet, compressed_size = self.rohc_module.compressor.compress_packet(packet)
            decompressed_packet = self.rohc_module.decompressor.decompress_packet(compressed_packet)
            simulation_events.append(f"Compressed: {compressed_packet}")
            simulation_events.append(f"Decompressed: {decompressed_packet}")
            
            scenario = self.automation_framework.scenario_generator.generate_scenario("5G_ROHC_Test")
            test_result = self.automation_framework.test_execution_engine.execute_test(scenario, packet)
            simulation_events.append(f"Test result: {test_result}")
            
            latency_value = f"{random.uniform(5, 15):.2f}ms"
            throughput_value = f"{random.uniform(100, 500):.2f}Mbps"
            self.test_framework.metrics_collector.collect_metric("Latency", latency_value)
            self.test_framework.metrics_collector.collect_metric("Throughput", throughput_value)
            
            metrics = self.test_framework.metrics_collector.metrics
            visualization = self.test_framework.results_visualization.visualize_results(metrics, packet_size)
            simulation_events.append(f"Visualization: {visualization}")
            
            report = self.automation_framework.report_generator.generate_detailed_report(simulation_events, metrics, ra_metrics)
            print(report)  # Output report to console
            return report
        
        except Exception as e:
            logging.error(f"Simulation failed: {str(e)}")
            return f"Simulation failed: {str(e)}"

if __name__ == "__main__":
    simulation = NS342ROHCSimulation()
    simulation.run_simulation()
