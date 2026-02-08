# TEAM XORCISTS

# 🏭 GenTwin — Generative Digital Twin Cybersecurity Analyzer

GenTwin is a hackathon prototype that combines **Digital Twin modeling** with an **AI-assisted reasoning engine** to uncover hidden cybersecurity gaps and attack propagation paths in industrial and cyber-physical systems.

Instead of relying on CVE databases or signature-only detection, GenTwin builds a structural twin from telemetry datasets, detects abnormal behavior, maps compromise spread across components, and produces reasoning-driven impact and mitigation insights.

---

# 🚩 Problem Statement

Industrial and cyber-physical systems often lack:

- system-level attack propagation visibility  
- cross-component risk reasoning  
- dataset-driven vulnerability discovery  
- structural security gap mapping  

Traditional security tools typically focus on:

- CVE lookup
- signature detection
- device-level scanning

These approaches miss **behavioral anomalies** and **system-wide compromise paths**.

GenTwin addresses this by combining:
Telemetry Data
→ Digital Twin Graph
→ Deviation Analysis
→ Compromise Mapping
→ Attack Chain Derivation
→ AI Reasoning Layer
→ Risk + Mitigation Output
---

# 🧠 Core Concept

GenTwin creates a **Digital Twin graph** from dataset features and uses deviation signals to simulate how compromise spreads across components. A reasoning layer then explains:

- likely impact
- security gaps
- mitigation strategies
- overall risk score

This produces **system-aware cybersecurity insights** rather than isolated alerts.

---

# ⚙️ Architecture Overview
Input Dataset (CSV telemetry)
↓
Auto Component Mapper
↓
Digital Twin Graph Builder
↓
Deviation / Anomaly Analyzer
↓
Compromised Node Detection
↓
Attack Chain Derivation
↓
AI Reasoning Engine
↓
Risk + Impact + Mitigation Output
↓
Interactive Dashboard UI
---

# 🧩 Project Structure
twin/ → digital twin builder
attack/ → anomaly + attack chain engine
ai/ → reasoning engine
ui/ → Streamlit dashboard
data/ → sample test datasets

---

# 🔬 Module Details

## 📁 twin/ — Digital Twin Builder

- auto-classifies dataset columns into component types
- builds graph of sensors, actuators, control nodes
- dataset-agnostic mapping logic
- exports `twin_graph.json`

---

## 📁 attack/ — Attack Analyzer

- compares baseline vs late-window telemetry
- computes deviation scores
- finds top changed components
- maps to twin graph nodes
- derives attack chain
- computes risk score and level
- exports `attack_paths.json`

---

## 📁 ai/ — AI Reasoning Engine

Rule-guided reasoning layer that produces:

- AI attack narrative
- impact summary
- mitigation suggestions
- discovered security gaps
- confidence score

Uses component-type knowledge rules (sensor / actuator / control).

---

## 📁 ui/ — Dashboard

Streamlit dashboard showing:

- risk metrics
- attack chain
- compromised components
- AI reasoning output
- mitigation & gap panels
- propagation graph visualization

---

# ✨ Key Features

- ✅ Digital twin built automatically from dataset schema  
- ✅ Dataset-agnostic engine design  
- ✅ Graph-based attack propagation modeling  
- ✅ AI-assisted impact & mitigation reasoning  
- ✅ System-level risk scoring  
- ✅ Modular pipeline architecture  
- ✅ Interactive visualization dashboard  

---

# 🆚 Difference from CVE Scanners

| Traditional CVE Tools | GenTwin |
|-----------------------|----------|
Known vulnerability lookup | Dataset-driven discovery |
Device focused | System focused |
Signature based | Behavior deviation based |
Static analysis | Structural propagation aware |
No reasoning layer | AI reasoning output |

---

# 📊 Expected Input Dataset Format

CSV with:

- numeric telemetry columns
- sensor / actuator / control signals
- one label column containing:
  - `Attack`
  - `Normal`

Example feature names:

---

# 🔬 Module Details

## 📁 twin/ — Digital Twin Builder

- auto-classifies dataset columns into component types
- builds graph of sensors, actuators, control nodes
- dataset-agnostic mapping logic
- exports `twin_graph.json`

---

## 📁 attack/ — Attack Analyzer

- compares baseline vs late-window telemetry
- computes deviation scores
- finds top changed components
- maps to twin graph nodes
- derives attack chain
- computes risk score and level
- exports `attack_paths.json`

---

## 📁 ai/ — AI Reasoning Engine

Rule-guided reasoning layer that produces:

- AI attack narrative
- impact summary
- mitigation suggestions
- discovered security gaps
- confidence score

Uses component-type knowledge rules (sensor / actuator / control).

---

## 📁 ui/ — Dashboard

Streamlit dashboard showing:

- risk metrics
- attack chain
- compromised components
- AI reasoning output
- mitigation & gap panels
- propagation graph visualization

---

# ✨ Key Features

- ✅ Digital twin built automatically from dataset schema  
- ✅ Dataset-agnostic engine design  
- ✅ Graph-based attack propagation modeling  
- ✅ AI-assisted impact & mitigation reasoning  
- ✅ System-level risk scoring  
- ✅ Modular pipeline architecture  
- ✅ Interactive visualization dashboard  

---

# 🆚 Difference from CVE Scanners

| Traditional CVE Tools | GenTwin |
|-----------------------|----------|
Known vulnerability lookup | Dataset-driven discovery |
Device focused | System focused |
Signature based | Behavior deviation based |
Static analysis | Structural propagation aware |
No reasoning layer | AI reasoning output |

---

# 📊 Expected Input Dataset Format

CSV with:

- numeric telemetry columns
- sensor / actuator / control signals
- one label column containing:
  - `Attack`
  - `Normal`

Example feature names:

LIT101 level sensor
AIT201 analyzer
P101 pump
MV201 valve
TEMP temperature
FLOW flow rate

Engine auto-maps component types from names.

---

# ▶️ How to Run

## 1️⃣ Build Digital Twin

```bash
python twin/twin_builder.py

Output: twin_graph.json

 Run Attack Analyzer:
python attack/attack_engine.py

Output: attack_paths.json

Run AI Reasoning:
python ai/ai_explainer.py

Launch Dashboard:
streamlit run ui/app.py

🧪 Validation

The engine was tested on multiple synthetic datasets to verify:

cross-domain component mapping

universal twin construction

stable attack chain derivation

consistent reasoning outputs

Test domains include:

HVAC systems

factory telemetry

datacenter metrics

pipeline sensors

power grid signals

🚀 Novel Contributions

Dataset-driven digital twin construction

Graph-based compromise propagation modeling

AI reasoning over system structure

Cross-component security gap inference

Domain-agnostic cyber-physical analysis

⚠️ Limitations

Prototype reasoning engine (rule-guided, not full LLM)

Not a production vulnerability scanner

Depends on telemetry quality

Twin topology is inferred, not real wiring

Mitigations are advisory suggestions

🔮 Future Work

Real-time telemetry ingestion

LLM-based reasoning integration

Temporal attack simulation

Automated mitigation planning

SOC workflow integration

Adaptive topology learning

👥 Team

Digital Twin Engine

Attack Analyzer

AI Reasoning Layer

Visualization Dashboard
