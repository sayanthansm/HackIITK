import pandas as pd
import networkx as nx
import json
import os
import sys

# --- add project root to path ---
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from twin.auto_mapper import classify_column

# ---------- load dataset ----------
DATA_PATH = os.path.join(ROOT_DIR, "data", "test_datacenter.csv")  
# change filename here when testing different datasets

print("Loading dataset:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

# ---------- build graph ----------
G = nx.Graph()

# ---------- add nodes ----------
for col in df.columns:
    if "ATTACK" in col.upper():
        continue

    ctype = classify_column(col)
    G.add_node(col, type=ctype)

# ---------- connect graph ----------
sensors = [n for n,d in G.nodes(data=True) if d["type"]=="SENSOR"]
acts    = [n for n,d in G.nodes(data=True) if d["type"]=="ACTUATOR"]
controls= [n for n,d in G.nodes(data=True) if d["type"]=="CONTROL"]

for s in sensors:
    for a in acts[:3]:
        G.add_edge(s, a)

for a in acts:
    for c in controls[:2]:
        G.add_edge(a, c)

print("Sensors:", len(sensors))
print("Actuators:", len(acts))
print("Controls:", len(controls))
print("Total nodes:", len(G.nodes))

# ---------- export ----------
data = nx.node_link_data(G)

OUT_PATH = os.path.join(ROOT_DIR, "twin_graph.json")
with open(OUT_PATH, "w") as f:
    json.dump(data, f, indent=2)

print("Twin graph exported →", OUT_PATH)
