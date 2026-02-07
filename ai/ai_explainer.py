import json
import random
import os

random.seed(42)
KNOWLEDGE_BASE = {
    "PLC": {
        "impacts": [
            "unauthorized modification of control logic",
            "malicious alteration of PLC execution flow"
        ],
        "mitigations": [
            "isolate the affected PLC from the control network",
            "verify ladder logic integrity",
            "enforce signed firmware updates"
        ],
        "gap": "absence of runtime PLC integrity monitoring",
        "severity": 5
    },
    "SENSOR": {
        "impacts": [
            "false process state reporting",
            "manipulation of sensor telemetry"
        ],
        "mitigations": [
            "enable sensor redundancy checks",
            "apply anomaly-based sanity thresholds"
        ],
        "gap": "lack of sensor authentication mechanisms",
        "severity": 3
    },
    "ACTUATOR": {
        "impacts": [
            "unsafe physical actuation",
            "unintended mechanical operations"
        ],
        "mitigations": [
            "validate actuator command sequences",
            "enable physical safety interlocks"
        ],
        "gap": "missing actuator safety override controls",
        "severity": 4
    }
}

def generate_explanation(attack_chain):
    templates = [
        "The attack path demonstrates coordinated compromise across {} components, enabling physical process manipulation.",
        "Analysis reveals lateral movement through {}, increasing the likelihood of unsafe operational states.",
        "The observed sequence across {} indicates a high-risk cyber-physical attack scenario."
    ]

    components = ", ".join(set(
        "PLC" if "PLC" in n.upper() else
        "SENSOR" if "SENSOR" in n.upper() else
        "ACTUATOR" if "ACTUATOR" in n.upper() else
        "CONTROL"
        for n in attack_chain
    ))

    return random.choice(templates).format(components)

def run_genai_reasoning(attack_chain, base_risk):
    impacts = []
    mitigations = []
    gaps = set()
    risk = base_risk

    for node in attack_chain:
        node_upper = node.upper()
        for key, rule in KNOWLEDGE_BASE.items():
            if key in node_upper:
                impacts.append(random.choice(rule["impacts"]))
                mitigations.append(random.choice(rule["mitigations"]))
                gaps.add(rule["gap"])
                risk += rule["severity"]

    final_risk = min(risk, 10)

    confidence = round(min(0.5 + (final_risk / 20), 0.95), 2)

    return {
        "ai_explanation": generate_explanation(attack_chain),
        "impact_summary": list(set(impacts)),
        "mitigation_suggestions": list(set(mitigations)),
        "discovered_gaps": list(gaps),
        "final_risk_score": final_risk,
        "confidence": confidence
    }

def generate_ai_report(attack_path_json):
    with open(attack_path_json, "r") as f:
        data = json.load(f)

    if "attack_chain" not in data or "risk_score" not in data:
        raise ValueError("Invalid input format: attack_chain or risk_score missing")

    return {
        "attack_chain": data["attack_chain"],
        "base_risk_score": data["risk_score"],
        **run_genai_reasoning(
            data["attack_chain"],
            data["risk_score"]
        )
    }

"""
BASE_DIR = os.path.dirname(__file__)
ATTACK_PATH_FILE = os.path.join(BASE_DIR, "attack_paths.json")

report = generate_ai_report(ATTACK_PATH_FILE)

print(report)
"""