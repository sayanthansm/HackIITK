# TEAM XORCISTS

# 🏭 GenTwin — GAN-Powered Generative Digital Twin Cybersecurity Analyzer

GenTwin is a hackathon prototype that combines **Digital Twin modeling**, **GAN-based anomaly detection**, and an **AI-assisted reasoning engine** to uncover hidden cybersecurity gaps and attack propagation paths in industrial and cyber-physical systems.

Instead of relying on CVE databases or signature-only detection, GenTwin learns normal telemetry behavior using a **Generative Adversarial Network (GAN)**, detects anomalies through reconstruction error, maps compromise spread across system components, and produces reasoning-driven impact and mitigation insights.

---

# 🚩 Problem Statement

Industrial and cyber-physical systems often lack:

* system-level attack propagation visibility
* cross-component risk reasoning
* dataset-driven anomaly discovery
* structural security gap mapping

Traditional security tools typically focus on:

* CVE lookup
* signature detection
* device-level scanning

These approaches miss **behavioral anomalies** and **system-wide compromise paths**.

GenTwin addresses this using:

Telemetry Data
→ GAN Normal Behavior Learning
→ Digital Twin Graph
→ GAN Anomaly Scoring
→ Compromise Mapping
→ Attack Chain Derivation
→ AI Reasoning Layer
→ Risk + Mitigation Output

---

# 🧠 Core Concept

GenTwin builds a **Digital Twin graph** from telemetry features and trains a **GAN on baseline (normal) telemetry** to learn the system’s normal operational distribution.

During analysis:

* GAN generator reconstruction error is used as anomaly signal
* High-error signals are marked as compromised components
* Compromise spreads across the twin graph
* AI reasoning explains impact, gaps, and mitigations

This produces **system-aware cybersecurity insights**, not isolated alerts.

---

# ⚙️ Architecture Overview

Input Dataset (CSV telemetry)
↓
Auto Component Mapper
↓
Digital Twin Graph Builder
↓
**GAN Training on Normal Telemetry**
↓
GAN Reconstruction Error Anomaly Scoring
↓
Compromised Node Detection
↓
Attack Chain Derivation (Graph Propagation)
↓
AI Reasoning Engine
↓
Risk + Impact + Mitigation Output
↓
Interactive Dashboard UI

---

# 🤖 GAN Role in the System

GenTwin uses a lightweight GAN to model normal telemetry behavior.

**Training Phase**

* Train GAN on normal telemetry window
* Generator learns feature distribution
* Scaler saved for runtime normalization

**Detection Phase**

* Recent telemetry is scaled
* Generator produces reconstructed signals
* Reconstruction error = anomaly score
* Top anomaly features → compromised nodes

This enables:

* behavior-based anomaly detection
* dataset-driven threat discovery
* signature-independent detection

---

# 🧩 Project Structure

```
twin/     → digital twin builder
attack/   → GAN anomaly + attack chain engine
ai/       → reasoning engine
ui/       → Streamlit dashboard
data/     → datasets
gan_train.py → GAN training module
```

---

# 🔬 Module Details

## 📁 twin/ — Digital Twin Builder

* auto-classifies dataset columns into component types
* builds graph of sensors, actuators, control nodes
* dataset-agnostic mapping logic
* exports `twin_graph.json`

---

## 📁 attack/ — GAN Attack Analyzer

* loads trained GAN + scaler
* computes reconstruction error anomaly scores
* ranks anomalous components
* maps anomalies to twin graph nodes
* derives attack propagation chain
* computes risk score and level
* exports `attack_paths.json`

Detection method recorded as:

```
GAN_reconstruction_error
```

---

## 📁 ai/ — AI Reasoning Engine

Rule-guided reasoning layer that produces:

* AI attack narrative
* impact summary
* mitigation suggestions
* discovered security gaps
* confidence score

Reasoning is component-type aware (sensor / actuator / control).

---

## 📁 ui/ — Dashboard

Streamlit dashboard showing:

* risk metrics
* attack chain
* compromised components
* GAN-based detection flag
* AI reasoning output
* mitigation & gap panels
* propagation graph visualization

---

# ✨ Key Features

* ✅ GAN-based anomaly detection
* ✅ Digital twin built automatically from dataset schema
* ✅ Behavior-driven threat discovery
* ✅ Graph-based attack propagation modeling
* ✅ AI-assisted impact & mitigation reasoning
* ✅ System-level risk scoring
* ✅ Dataset-agnostic design
* ✅ Modular pipeline architecture
* ✅ Interactive visualization dashboard

---

# 🆚 Difference from CVE Scanners

| Traditional CVE Tools      | GenTwin                |
| -------------------------- | ---------------------- |
| Known vulnerability lookup | GAN behavior learning  |
| Device focused             | System focused         |
| Signature based            | Behavior anomaly based |
| Static scan                | Telemetry-driven       |
| No propagation model       | Twin graph propagation |
| No reasoning layer         | AI reasoning output    |

---

# 📊 Expected Input Dataset Format

CSV with:

* numeric telemetry columns
* sensor / actuator / control signals
* one label column containing:

  * Attack
  * Normal

Example feature names:

```
LIT101
AIT201
P101
MV201
TEMP
FLOW
```

Component types are auto-mapped from names.

---

# ▶️ How to Run

## 1️⃣ Train GAN

```bash
python gan_train.py
```

Outputs:

```
gan_generator.pt
gan_scaler.pkl
```

---

## 2️⃣ Build Digital Twin

```bash
python twin/twin_builder.py
```

Output:

```
twin_graph.json
```

---

## 3️⃣ Run Attack Analyzer (GAN Enabled)

```bash
python attack/attack_engine.py
```

Output:

```
attack_paths.json
```

---

## 4️⃣ Run AI Reasoning

```bash
python ai/ai_explainer.py
```

---

## 5️⃣ Launch Dashboard

```bash
streamlit run ui/app.py
```

---

# 🧪 Validation

Tested across synthetic cross-domain datasets:

* HVAC systems
* factory telemetry
* datacenter metrics
* pipeline sensors
* power grid signals

Validated for:

* twin construction stability
* GAN anomaly ranking
* attack chain derivation
* reasoning consistency

---

# 🚀 Novel Contributions

* GAN-based telemetry anomaly detection
* Dataset-driven digital twin construction
* Graph-based compromise propagation modeling
* AI reasoning over system structure
* Cross-domain cyber-physical analysis
* Behavior-first security discovery

---

# ⚠️ Limitations

* Lightweight GAN (hackathon scale)
* Rule-guided reasoning engine
* Not a production vulnerability scanner
* Twin topology is inferred
* Mitigations are advisory

---

# 🔮 Future Work

* Real-time telemetry streaming
* LLM reasoning integration
* temporal attack simulation
* automated mitigation planning
* SOC workflow integration
* adaptive topology learning

---

# 👥 Team XORCISTS

Digital Twin Engine
GAN Detection Engine
Attack Analyzer
AI Reasoning Layer
Visualization Dashboard

---
