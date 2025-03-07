# header_compression.py
import rohc

def header_compression_example():
    # Build a dummy IPv4 packet (20-byte header + payload).
    ip_header = bytearray(20)
    ip_header[0] = 0x45              # IPv4, IHL = 5 (20 bytes)
    ip_header[1] = 0                 # DSCP/ECN
    ip_header[2:4] = (20).to_bytes(2, byteorder='big')  # Total length (for header only)
    ip_header[9] = 17                # Protocol (e.g., UDP)
    ip_header[12:16] = b'\xc0\xa8\x01\x02'  # Source IP: 192.168.1.2
    ip_header[16:20] = b'\xc0\xa8\x01\x01'  # Destination IP: 192.168.1.1
    payload = b"Hello, ROHC Header Compression!"
    packet = bytes(ip_header) + payload

    print("Original Packet:", packet.hex())

    # Compress the packet using our simple ROHC implementation.
    compressed_packet = rohc.compress(packet)
    print("Compressed Packet:", compressed_packet.hex())

    # Decompress the packet.
    decompressed_packet = rohc.decompress(compressed_packet)
    print("Decompressed Packet:", decompressed_packet.hex())

if __name__ == "__main__":
    header_compression_example()
