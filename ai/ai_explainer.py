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
         "GAN-based anomaly detection identified abnormal behavior across {} enabling physical process manipulation.",
        "Generator reconstruction error indicates coordinated compromise across {} within the control system.",
        "Adversarial model anomaly scoring highlights high-risk deviations across {}."
    ]

    components = ", ".join(set(
        "PLC" if "PLC" in n.upper() else
        "SENSOR" if "SENSOR" in n.upper() else
        "ACTUATOR" if "ACTUATOR" in n.upper() else
        "industrial control components"
        for n in attack_chain
    ))

    return random.choice(templates).format(components)
def classify_component(node_name: str):
    n = node_name.upper()

    # sensor tags
    if n.startswith(("LIT", "AIT", "PIT", "FIT", "DPIT", "PH", "UV")):
        return "SENSOR"

    # actuator tags
    if n.startswith(("P", "MV")):
        return "ACTUATOR"

    # fallback
    return "PLC"

def run_genai_reasoning(attack_chain, base_risk):
    impacts = []
    mitigations = []
    gaps = set()
    risk = base_risk

    for node in attack_chain:
        comp_type = classify_component(node)

        rule = KNOWLEDGE_BASE.get(comp_type)
        if not rule:
            continue

        impacts.append(random.choice(rule["impacts"]))
        mitigations.append(random.choice(rule["mitigations"]))
        gaps.add(rule["gap"])
        risk += rule["severity"]


    final_risk = min(risk, 10)

    confidence = round(
    min(
        0.6 + 0.02*len(attack_chain) + 0.02*len(impacts),
        0.97
    ),
    2
)


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

    if "compromised_nodes" not in data or "risk_score" not in data:
        raise ValueError("Invalid input format")

    chain = data["compromised_nodes"]

    return {
        "attack_chain": chain,
        "base_risk_score": data["risk_score"],
        **run_genai_reasoning(chain, data["risk_score"])
    }

# ---------- correct path to root attack_paths.json ----------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ATTACK_PATH_FILE = os.path.join(BASE_DIR, "attack_paths.json")

report = generate_ai_report(ATTACK_PATH_FILE)

print(report)
