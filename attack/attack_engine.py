import pandas as pd
import os
import numpy as np

# ---------- load ----------
df = pd.read_csv("data/swat_attack.csv")

# ---------- find label column ----------
label_col = None
for c in df.columns:
    if "ATTACK" in c.upper():
        label_col = c
        break

print("Label column:", label_col)

attack_rows = df[df[label_col] == "Attack"]
normal_rows = df[df[label_col] == "Normal"]

print("Total rows:", len(df))
print("Attack rows:", len(attack_rows))
print("Normal rows:", len(normal_rows))


# ---------- numeric-only selection ----------
numeric_df = df.select_dtypes(include="number")

print("\nNumeric columns:", len(numeric_df.columns))

# ---------- baseline vs late window ----------
baseline = numeric_df.iloc[:1000].mean()
late = numeric_df.iloc[-1000:].mean()

# ---------- deviation ----------
deviation = (late - baseline).abs()

top_changed = deviation.sort_values(ascending=False).head(15)

print("\nTop changed components during attack:\n")
for name, val in top_changed.items():
    print(name, "Δ", round(val, 3))

import json
import networkx as nx

# ---------- load twin graph ----------
with open("twin_graph.json") as f:
    twin_data = json.load(f)

G = nx.node_link_graph(twin_data)

# ---------- mark compromised nodes ----------
compromised = []

for comp in top_changed.index:
    if comp in G.nodes:
        G.nodes[comp]["compromised"] = True
        compromised.append(comp)

print("\nCompromised nodes found in twin:", compromised)


# ---------- derive attack stages ----------
comp_stages = set()

for node in compromised:
    for parent in G.predecessors(node):
        if G.nodes[parent].get("type") == "stage":
            comp_stages.add(parent)

attack_path = sorted(comp_stages)

print("\nAttack path stages:", attack_path)


risk_score = len(compromised) + 2*len(attack_path)

if risk_score >= 20:
    risk_level = "HIGH"
elif risk_score >= 10:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"

summary = f"""
Attack affects {len(compromised)} components across {len(attack_path)} process stages.
Primary impact stages: {", ".join(attack_path)}.
Overall risk level: {risk_level}.
"""

attack_report = {
    "compromised_nodes": compromised,
    "attack_stages": attack_path,
    "risk_score": risk_score,
    "risk_level": risk_level,
    "summary": summary.strip()
}

with open("attack_paths.json","w") as f:
    json.dump(attack_report, f, indent=2)

print("\nattack_paths.json exported")
