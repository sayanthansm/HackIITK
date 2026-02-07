import networkx as nx
import json

# create directed graph
G = nx.DiGraph()

# define SWaT stages
stages = ["P1","P2","P3","P4","P5","P6"]

# add stage nodes
for s in stages:
    G.add_node(s, type="stage", criticality="high")

# connect stages in flow order
for i in range(len(stages)-1):
    G.add_edge(stages[i], stages[i+1], relation="flow")

print("Nodes:")
print(G.nodes(data=True))

print("\nEdges:")
print(list(G.edges()))

# export graph
data = nx.node_link_data(G)

with open("twin_graph.json","w") as f:
    json.dump(data,f,indent=2)

print("\nTwin graph exported → twin_graph.json")
