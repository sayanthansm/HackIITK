import pandas as pd
import networkx as nx
import json

# ---------- load dataset ----------
df = pd.read_csv("data/swat_attack.csv")

# ---------- build graph ----------
G = nx.DiGraph()

stages = ["P1","P2","P3","P4","P5","P6"]

for s in stages:
    G.add_node(s, type="stage", criticality="high")

for i in range(len(stages)-1):
    G.add_edge(stages[i], stages[i+1], relation="flow")

# ---------- classify columns ----------
sensor_cols = []
actuator_cols = []

for c in df.columns:
    cu = c.upper()

    if cu.startswith(("AIT","FIT","LIT","PIT","DPIT","PH","UV")):
        sensor_cols.append(c)

    elif cu.startswith(("MV","P")):
        actuator_cols.append(c)

print("Sensors found:", len(sensor_cols))
print("Actuators found:", len(actuator_cols))

# ---------- add sensors ----------
for s in sensor_cols:
    stage = "P" + s[-3] if s[-3].isdigit() else "P1"
    if stage not in stages:
        stage = "P1"

    G.add_node(s, type="sensor", criticality="medium")
    G.add_edge(stage, s, relation="has_sensor")

# ---------- add actuators ----------
for a in actuator_cols:
    stage = "P" + a[-3] if a[-3].isdigit() else "P1"
    if stage not in stages:
        stage = "P1"

    G.add_node(a, type="actuator", criticality="high")
    G.add_edge(stage, a, relation="controls")

print("Total graph nodes:", len(G.nodes))

# ---------- export ----------
data = nx.node_link_data(G)

with open("twin_graph.json","w") as f:
    json.dump(data,f,indent=2)

print("Twin graph exported with components")
