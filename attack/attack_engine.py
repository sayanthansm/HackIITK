import pandas as pd
import numpy as np
import json
import networkx as nx
import os

# -----------------------------
# CONFIG — change dataset here
# -----------------------------
DATA_PATH = "data/test_pipeline.csv"

print("Loading dataset:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

# -----------------------------
# find label column
# -----------------------------
label_col = None
for c in df.columns:
    if "ATTACK" in c.upper():
        label_col = c
        break

if not label_col:
    raise ValueError("No Attack label column found")

print("Label column:", label_col)

attack_rows = df[df[label_col] == "Attack"]
normal_rows = df[df[label_col] == "Normal"]

print("Total rows:", len(df))
print("Attack rows:", len(attack_rows))
print("Normal rows:", len(normal_rows))

# -----------------------------
# numeric-only selection
# -----------------------------
numeric_df = df.select_dtypes(include="number")

print("\nNumeric columns:", len(numeric_df.columns))

if len(numeric_df.columns) == 0:
    raise ValueError("No numeric columns found")

# -----------------------------
# baseline vs late window
# -----------------------------
window = min(1000, len(numeric_df)//2)

baseline = numeric_df.iloc[:window].mean()
late = numeric_df.iloc[-window:].mean()

# -----------------------------
# deviation
# -----------------------------
deviation = (late - baseline).abs()

top_changed = deviation.sort_values(ascending=False).head(15)

print("\nTop changed components during attack:\n")
for name, val in top_changed.items():
    print(name, "Δ", round(val, 3))

# -----------------------------
# load twin graph
# -----------------------------
if not os.path.exists("twin_graph.json"):
    raise FileNotFoundError("Run twin_builder.py first")

with open("twin_graph.json") as f:
    twin_data = json.load(f)

G = nx.node_link_graph(twin_data)

print("\nTwin nodes:", len(G.nodes))

# -----------------------------
# mark compromised nodes
# -----------------------------
compromised = []

for comp in top_changed.index:
    if comp in G.nodes:
        compromised.append(comp)
        G.nodes[comp]["compromised"] = True

print("\nCompromised nodes found in twin:", compromised)

# -----------------------------
# derive attack propagation chain
# -----------------------------
attack_chain = set(compromised)

for node in compromised:
    neighbors = list(G.neighbors(node))
    attack_chain.update(neighbors)

attack_chain = sorted(attack_chain)

print("\nAttack propagation chain:", attack_chain)

# -----------------------------
# risk scoring
# -----------------------------
risk_score = len(compromised) + len(attack_chain)

if risk_score >= 20:
    risk_level = "HIGH"
elif risk_score >= 10:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"

summary = f"""
Attack affects {len(compromised)} components and propagates across
{len(attack_chain)} connected assets in the digital twin.
Overall risk level: {risk_level}.
"""

# -----------------------------
# export report
# -----------------------------
attack_report = {
    "compromised_nodes": compromised,
    "attack_chain": attack_chain,
    "risk_score": risk_score,
    "risk_level": risk_level,
    "summary": summary.strip()
}

with open("attack_paths.json","w") as f:
    json.dump(attack_report, f, indent=2)

print("\nattack_paths.json exported")
