from Crypto.Cipher import AES
from Crypto.Hash import CMAC

def generate_mac(message: bytes, key: bytes) -> bytes:
    """
    Generate MAC-I using AES-CMAC (NIA2 Integrity Algorithm).
    :param message: The PDCP PDU (Header + SDU) as bytes.
    :param key: The 128-bit integrity key.
    :return: The 4-byte MAC-I.
    """
    cmac = CMAC.new(key, ciphermod=AES)
    cmac.update(message)
    return cmac.digest()[:4]  # Extract 4-byte MAC-I

def verify_mac(received_mac: bytes, computed_mac: bytes) -> bool:
    """
    Verify MAC-I at the receiving end.
    :param received_mac: The received MAC-I from sender.
    :param computed_mac: The computed MAC-I at the receiver.
    :return: True if valid, False otherwise.
    """
    return received_mac == computed_mac

# Example Usage
if __name__ == "__main__":
    # Example 128-bit Integrity Key (Should be securely derived in real cases)
    integrity_key = bytes.fromhex("2B7E151628AED2A6ABF7158809CF4F3C")
    
    # Example PDCP PDU (Header + SDU)
    pdcp_pdu = b"This is PDCP data"  # Replace with actual PDCP payload
    
    # Sender Side: Generate MAC-I
    mac_i = generate_mac(pdcp_pdu, integrity_key)
    print("Generated MAC-I:", mac_i.hex())
    
    # Receiver Side: Compute XMAC-I and Verify
    computed_mac = generate_mac(pdcp_pdu, integrity_key)
    is_valid = verify_mac(mac_i, computed_mac)
    print("Integrity Verification:", "Valid" if is_valid else "Invalid")

