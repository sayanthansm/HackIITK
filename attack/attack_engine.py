import pandas as pd
import json
import networkx as nx
import os
import pickle
import torch
import torch.nn as nn

DATA_PATH = "data/swat_attack.csv"
LATENT_DIM = 32   # MUST match gan_train.py

print("Loading dataset:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

# -------- label detect --------
label_col = None
for c in df.columns:
    if "ATTACK" in c.upper():
        label_col = c
        break

labels = df[label_col].astype(str).str.upper()
attack_rows = df[labels.str.contains("ATTACK")]
normal_rows = df[labels.str.contains("NORMAL")]

print("Attack rows:", len(attack_rows))
print("Normal rows:", len(normal_rows))

numeric_df = df.select_dtypes(include="number")
INPUT_DIM = len(numeric_df.columns)

# -------- Generator (MATCH TRAINING) --------
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(LATENT_DIM, 128),
            nn.ReLU(),
            nn.Linear(128, INPUT_DIM)
        )

    def forward(self, z):
        return self.net(z)

gan_model = None

# -------- load GAN --------
if os.path.exists("gan_generator.pt") and os.path.exists("gan_scaler.pkl"):

    with open("gan_scaler.pkl","rb") as f:
        scaler = pickle.load(f)

    gan_model = Generator()
    gan_model.load_state_dict(
        torch.load("gan_generator.pt", map_location="cpu")
    )
    gan_model.eval()

    print("✅ GAN loaded")

else:
    print("⚠️ GAN missing — fallback mode")

# -------- anomaly scoring --------
window = min(1000, len(numeric_df)//2)
recent = numeric_df.iloc[-window:]

if gan_model:

    scaled = scaler.transform(recent.values)
    t = torch.tensor(scaled, dtype=torch.float32)

    # project into latent space randomly and reconstruct
    z = torch.randn(len(t), LATENT_DIM)

    with torch.no_grad():
        recon = gan_model(z)

    err = torch.mean((t - recon)**2, dim=0)

    scores = dict(zip(numeric_df.columns, err.numpy()))
    top_changed = sorted(scores.items(), key=lambda x:x[1], reverse=True)[:15]

else:
    base = numeric_df.iloc[:window].mean()
    late = numeric_df.iloc[-window:].mean()
    dev = (late-base).abs()
    top_changed = list(dev.sort_values(ascending=False).head(15).items())

print("\nTop anomalous components:")
for n,v in top_changed:
    print(n, round(float(v),3))

# -------- twin graph --------
with open("twin_graph.json") as f:
    G = nx.node_link_graph(json.load(f))

compromised = []
for comp,_ in top_changed:
    if comp in G.nodes:
        compromised.append(comp)

attack_chain = set(compromised)
for n in compromised:
    attack_chain.update(G.neighbors(n))

attack_chain = sorted(attack_chain)

risk_score = len(compromised)+len(attack_chain)
risk_level = "HIGH" if risk_score>=20 else "MEDIUM" if risk_score>=10 else "LOW"

attack_report = {
    "compromised_nodes": compromised,
    "attack_chain": attack_chain,
    "risk_score": risk_score,
    "risk_level": risk_level,
    "detection_method": "GAN_reconstruction_error" if gan_model else "statistical"
}

with open("attack_paths.json","w") as f:
    json.dump(attack_report,f,indent=2)

print("✅ attack_paths.json exported")
