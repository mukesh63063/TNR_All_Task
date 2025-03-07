import random
import matplotlib
matplotlib.use('Agg')  # Use Agg backend (non-interactive, file-only)
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Simulate HARQ process (simplified, no NS-3)
def simulate_harq(num_processes=4, num_transmissions=100):
    harq_logs = []
    for i in range(num_transmissions):
        process_id = random.randint(0, num_processes - 1)
        retrans_count = random.randint(0, 3)  # Simulate 0-3 retransmissions
        success = random.choice([True, False])  # Random ACK/NACK
        latency = retrans_count * 2 + 1  # Simplified latency (ms)
        harq_logs.append({
            "process_id": process_id,
            "retrans_count": retrans_count,
            "success": success,
            "latency": latency
        })
    return harq_logs

# Save logs to file
def save_logs(harq_logs, filepath="output/harq_logs.txt"):
    try:
        with open(filepath, "w") as f:
            f.write("ProcessID,Retransmissions,Success,Latency\n")
            for log in harq_logs:
                f.write(f"{log['process_id']},{log['retrans_count']},{log['success']},{log['latency']}\n")
        print(f"Logs saved to {filepath}")
    except Exception as e:
        print(f"Error saving logs: {e}")

# Analyze HARQ performance
def analyze_harq(harq_logs):
    total = len(harq_logs)
    successes = sum(1 for log in harq_logs if log["success"])
    success_rate = (successes / total) * 100 if total > 0 else 0
    avg_latency = sum(log["latency"] for log in harq_logs) / total if total > 0 else 0
    retrans_counts = [log["retrans_count"] for log in harq_logs]
    return success_rate, avg_latency, retrans_counts

# Plot retransmission trends
def plot_retransmissions(retrans_counts, filepath="output/harq_plot.png"):
    try:
        sns.histplot(retrans_counts, bins=4, kde=True)
        plt.title("HARQ Retransmission Trends")
        plt.xlabel("Number of Retransmissions")
        plt.ylabel("Frequency")
        plt.savefig(filepath)
        plt.close()
        print(f"Plot saved to {filepath}")
    except Exception as e:
        print(f"Error plotting: {e}")

# Generate summary report
def generate_report(success_rate, avg_latency, filepath="output/summary_report.txt"):
    try:
        with open(filepath, "w") as f:
            f.write("HARQ Performance Summary\n")
            f.write(f"Success Rate: {success_rate:.2f}%\n")
            f.write(f"Average Latency: {avg_latency:.2f} ms\n")
        print(f"Report saved to {filepath}")
    except Exception as e:
        print(f"Error saving report: {e}")

# Main function to run everything
def main():
    try:
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        print("Output directory ready")

        # Step 1 & 2: Simulate and capture HARQ data
        harq_logs = simulate_harq()
        save_logs(harq_logs)

        # Step 3 & 4: Analyze HARQ performance
        success_rate, avg_latency, retrans_counts = analyze_harq(harq_logs)

        # Step 5: Generate plot and report
        plot_retransmissions(retrans_counts)
        generate_report(success_rate, avg_latency)
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()