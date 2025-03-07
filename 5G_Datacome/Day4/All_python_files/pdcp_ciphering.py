from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util import Counter

def generate_mac(message: bytes, key: bytes) -> bytes:
    """
    Generate MAC-I using AES-CMAC (NIA2 Integrity Algorithm).
    :param message: The PDCP PDU (Header + SDU) as bytes.
    :param key: The 128-bit integrity key.
    :return: The 4-byte MAC-I.
    """
    cmac = CMAC.new(key, ciphermod=AES)
    cmac.update(message)
    return cmac.digest()[:4]  # Extract the first 4 bytes (MAC-I)

def verify_mac(received_mac: bytes, computed_mac: bytes) -> bool:
    """
    Verify MAC-I at the receiving end.
    :param received_mac: The received MAC-I from sender.
    :param computed_mac: The computed MAC-I at the receiver.
    :return: True if valid, False otherwise.
    """
    return received_mac == computed_mac

def encrypt_pdcp(data: bytes, key: bytes, count: int) -> bytes:
    """
    Encrypt PDCP PDU using AES-CTR mode (Ciphering in PDCP).
    :param data: The PDCP PDU (Header + SDU) as bytes.
    :param key: The 128-bit encryption key.
    :param count: The PDCP COUNT value (used as IV/Nonce).
    :return: Encrypted data.
    """
    ctr = Counter.new(128, initial_value=count)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(data)

def decrypt_pdcp(encrypted_data: bytes, key: bytes, count: int) -> bytes:
    """
    Decrypt PDCP PDU using AES-CTR mode (Ciphering in PDCP).
    :param encrypted_data: The encrypted PDCP PDU.
    :param key: The 128-bit encryption key.
    :param count: The PDCP COUNT value (used as IV/Nonce).
    :return: Decrypted data.
    """
    ctr = Counter.new(128, initial_value=count)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(encrypted_data)

# Example Usage
if __name__ == "__main__":
    # Example 128-bit Integrity and Ciphering Key (Should be securely derived in real cases)
    integrity_key = bytes.fromhex("2B7E151628AED2A6ABF7158809CF4F3C")
    ciphering_key = bytes.fromhex("3AD77BB40D7A3660A89ECAF32466EF97")
    
    # Example PDCP PDU (Header + SDU)
    pdcp_pdu = b"Hii 5G this is TEAM- Latency Leaders"  # Replace with actual PDCP payload
    
    # Sender Side: Generate MAC-I
    mac_i = generate_mac(pdcp_pdu, integrity_key)
    print("Generated MAC-I:", mac_i.hex())
    
    # Receiver Side: Compute XMAC-I and Verify
    computed_mac = generate_mac(pdcp_pdu, integrity_key)
    is_valid = verify_mac(mac_i, computed_mac)
    print("Integrity Verification:", "Valid" if is_valid else "Invalid")
    
    # Ciphering Example (Encryption and Decryption)
    count = 12345  # Example COUNT value
    encrypted_data = encrypt_pdcp(pdcp_pdu, ciphering_key, count)
    print("Encrypted PDCP Data:", encrypted_data.hex())
    
    decrypted_data = decrypt_pdcp(encrypted_data, ciphering_key, count)
    print("Decrypted PDCP Data:", decrypted_data.decode())
