import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import pickle
from sklearn.preprocessing import StandardScaler

# ---------------- CONFIG ----------------
DATA_PATH = "data/swat_attack.csv"
EPOCHS = 10
BATCH_SIZE = 128
LATENT_DIM = 32
LR = 0.0002

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", DEVICE)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# -------- label column detection --------
label_col = None
for c in df.columns:
    if "ATTACK" in c.upper():
        label_col = c
        break

print("Label column:", label_col)

# -------- choose normal rows safely --------
if label_col:
    labels = df[label_col].astype(str).str.upper()

    normal_df = df[labels.str.contains("NORMAL")]
    attack_df = df[labels.str.contains("ATTACK")]

    print("Normal rows:", len(normal_df))
    print("Attack rows:", len(attack_df))

else:
    normal_df = pd.DataFrame()

# -------- fallback if no normal rows --------
if len(normal_df) == 0:
    print("⚠️ No NORMAL rows found — using first 70% as baseline")
    normal_df = df.iloc[:int(len(df)*0.7)]

# -------- numeric only --------
numeric_df = normal_df.select_dtypes(include="number")

if len(numeric_df) == 0:
    raise ValueError("No numeric columns found")

print("Numeric features:", len(numeric_df.columns))

# ---------------- SCALE ----------------
scaler = StandardScaler()
scaled = scaler.fit_transform(numeric_df.values)

with open("gan_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

data_tensor = torch.tensor(scaled, dtype=torch.float32)
INPUT_DIM = data_tensor.shape[1]

# ---------------- MODELS ----------------
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


class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(INPUT_DIM, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)


G = Generator().to(DEVICE)
D = Discriminator().to(DEVICE)

criterion = nn.BCELoss()
g_opt = optim.Adam(G.parameters(), lr=LR)
d_opt = optim.Adam(D.parameters(), lr=LR)

loader = torch.utils.data.DataLoader(
    data_tensor,
    batch_size=BATCH_SIZE,
    shuffle=True,
    drop_last=True
)

# ---------------- TRAIN ----------------
for epoch in range(EPOCHS):

    g_loss_total = 0
    d_loss_total = 0

    for real in loader:

        real = real.to(DEVICE)
        bs = real.size(0)

        # ----- Train Discriminator -----
        z = torch.randn(bs, LATENT_DIM).to(DEVICE)
        fake = G(z).detach()

        d_real = D(real)
        d_fake = D(fake)

        real_lbl = torch.ones(bs,1).to(DEVICE)
        fake_lbl = torch.zeros(bs,1).to(DEVICE)

        d_loss = (criterion(d_real, real_lbl) +
                  criterion(d_fake, fake_lbl)) / 2

        d_opt.zero_grad()
        d_loss.backward()
        d_opt.step()

        # ----- Train Generator -----
        z = torch.randn(bs, LATENT_DIM).to(DEVICE)
        fake = G(z)
        pred = D(fake)

        g_loss = criterion(pred, real_lbl)

        g_opt.zero_grad()
        g_loss.backward()
        g_opt.step()

        g_loss_total += g_loss.item()
        d_loss_total += d_loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS} | D {d_loss_total:.3f} | G {g_loss_total:.3f}")

# ---------------- SAVE ----------------
torch.save(G.state_dict(), "gan_generator.pt")

print("\n✅ GAN training complete")
print("Saved gan_generator.pt")
print("Saved gan_scaler.pkl")
