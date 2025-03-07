import random

# 5QI Mapping for Different Services
SERVICE_5QI_MAPPING = {
    "Netflix": 4,
    "WhatsApp Video": 2,
    "Instagram": 6,
    "Amazon Prime": 4,
}

# DRB Allocation Based on QoS Type
def allocate_drb(qos_type):
    return f"{qos_type}-DRB{random.randint(1, 5)}"

# QoS Flow Mapping Storage
qfi_mappings = {}

# Function to Simulate RDI Testing in SDAP
def test_rdi(qfi, qos_type, service, rdi_value):
    if qfi in qfi_mappings:
        return f"❌ QFI {qfi} is already assigned to {qfi_mappings[qfi]['service']}! Cannot reuse."

    if service not in SERVICE_5QI_MAPPING:
        return "❌ Invalid service selected!"

    assigned_5qi = SERVICE_5QI_MAPPING[service]
    drb = allocate_drb(qos_type)
    reflective_qos = "Enabled" if rdi_value == 1 else "Disabled"
    rqi = random.choice(["Set", "Not Set"])

    # Store Mapping with RDI
    qfi_mappings[qfi] = {
        "qos_type": qos_type,
        "service": service,
        "5qi": assigned_5qi,
        "drb": drb,
        "rdi": rdi_value,
        "reflective_qos": reflective_qos,
        "rqi": rqi,
    }

    return f"✅ QFI {qfi} mapped to {service} (5QI: {assigned_5qi}) → {drb}, RDI: {rdi_value}, Reflective QoS: {reflective_qos}, RQI: {rqi}"

# Testing RDI Scenarios
test_cases = [
    (1, "GBR", "Netflix", 1),  # RDI Enabled
    (2, "GBR", "WhatsApp Video", 0),  # RDI Disabled
    (3, "Non-GBR", "Instagram", 1),  # RDI Enabled
    (4, "GBR", "Amazon Prime", 0),  # RDI Disabled
    (1, "GBR", "WhatsApp Video", 1),  # Duplicate QFI Test
]

# Running the RDI Tests
for qfi, qos_type, service, rdi_value in test_cases:
    print(test_rdi(qfi, qos_type, service, rdi_value))

# Display Final Mappings
print("\n📜 Final SDAP QoS Flow Mappings with RDI:")
for qfi, mapping in qfi_mappings.items():
    print(f"QFI {qfi} → {mapping}")
