import random

# QoS Templates (Grouping multiple services under common rules)
QOS_TEMPLATE_MAPPING = {
    "Streaming": {"5qi": 4, "qos_type": "GBR", "priority": 3},
    "Video Call": {"5qi": 2, "qos_type": "GBR", "priority": 1},
    "Social Media": {"5qi": 6, "qos_type": "Non-GBR", "priority": 5},
}

# DRB Allocation Based on QoS Type
def allocate_drb(qos_type):
    return f"{qos_type}-DRB{random.randint(1, 5)}"

# Storage for QTI assignments
qti_mappings = {}

# Function to Assign a QoS Template Identifier (QTI)
def assign_qti(qti, template_name):
    if qti in qti_mappings:
        return f"❌ QTI {qti} is already assigned to {qti_mappings[qti]['template']}! Cannot reuse."

    if template_name not in QOS_TEMPLATE_MAPPING:
        return "❌ Invalid QoS Template selected!"

    qos_settings = QOS_TEMPLATE_MAPPING[template_name]
    drb = allocate_drb(qos_settings["qos_type"])

    qti_mappings[qti] = {
        "template": template_name,
        "5qi": qos_settings["5qi"],
        "qos_type": qos_settings["qos_type"],
        "priority": qos_settings["priority"],
        "drb": drb,
    }

    return f"✅ QTI {qti} assigned to {template_name} → (5QI: {qos_settings['5qi']}, DRB: {drb}, Priority: {qos_settings['priority']})"

# Testing QTI Assignments
test_qti_cases = [
    (101, "Streaming"),
    (102, "Video Call"),
    (103, "Social Media"),
    (101, "Video Call"),  # Duplicate QTI Test
]

# Running the QTI Tests
for qti, template in test_qti_cases:
    print(assign_qti(qti, template))

# Display Final QTI Mappings
print("\n📜 Final QoS Template Mappings:")
for qti, mapping in qti_mappings.items():
    print(f"QTI {qti} → {mapping}")
