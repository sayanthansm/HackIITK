import pandas as pd
import numpy as np

np.random.seed(42)

def make_labels(n, attack_len):
    labels = ["Normal"]*n
    labels[-attack_len:] = ["Attack"]*attack_len
    return labels


# ---------------- POWER GRID ----------------
n=2500
pg = pd.DataFrame({
    "VOLT_A": np.random.normal(230,2,n),
    "CURR_A": np.random.normal(50,3,n),
    "TEMP_GEN": np.random.normal(70,1,n),
    "FREQ": np.random.normal(50,0.05,n),
    "BREAKER": np.random.choice([0,1],n,p=[0.9,0.1])
})
pg.iloc[-600:,0] += np.linspace(0,30,600)
pg.iloc[-600:,1] += np.linspace(0,25,600)
pg["Normal/Attack"] = make_labels(n,600)
pg.to_csv("data/test_powergrid.csv", index=False)


# ---------------- SMART FACTORY ----------------
n=2400
sf = pd.DataFrame({
    "MOTOR_RPM": np.random.normal(1800,50,n),
    "VIBRATION": np.random.normal(2,0.2,n),
    "LINE_PRESS": np.random.normal(5,0.3,n),
    "ROBOT_TEMP": np.random.normal(60,1,n),
    "VALVE": np.random.choice([0,1],n,p=[0.8,0.2])
})
sf.iloc[-500:,0] -= np.linspace(0,600,500)
sf.iloc[-500:,1] += np.linspace(0,3,500)
sf["Normal/Attack"] = make_labels(n,500)
sf.to_csv("data/test_factory.csv", index=False)


# ---------------- OIL PIPELINE ----------------
n=2600
op = pd.DataFrame({
    "PIPE_PRESS": np.random.normal(80,2,n),
    "FLOW_RATE": np.random.normal(300,10,n),
    "LEAK_SENSOR": np.random.normal(0.1,0.02,n),
    "PUMP_LOAD": np.random.normal(55,3,n),
    "PUMP": np.random.choice([0,1],n,p=[0.85,0.15])
})
op.iloc[-700:,0] -= np.linspace(0,40,700)
op.iloc[-700:,2] += np.linspace(0,1,700)
op["Normal/Attack"] = make_labels(n,700)
op.to_csv("data/test_pipeline.csv", index=False)


# ---------------- HVAC ----------------
n=2200
hv = pd.DataFrame({
    "ROOM_TEMP": np.random.normal(22,1,n),
    "AIRFLOW": np.random.normal(400,20,n),
    "CHILLER_LOAD": np.random.normal(70,3,n),
    "CO2": np.random.normal(500,30,n),
    "DAMPER": np.random.choice([0,1],n,p=[0.7,0.3])
})
hv.iloc[-500:,0] += np.linspace(0,10,500)
hv.iloc[-500:,1] -= np.linspace(0,150,500)
hv["Normal/Attack"] = make_labels(n,500)
hv.to_csv("data/test_hvac.csv", index=False)


# ---------------- DATA CENTER ----------------
n=2300
dc = pd.DataFrame({
    "CPU_LOAD": np.random.normal(40,5,n),
    "RACK_TEMP": np.random.normal(28,1,n),
    "POWER_DRAW": np.random.normal(5,0.5,n),
    "FAN_SPEED": np.random.normal(3000,200,n),
    "COOLING": np.random.choice([0,1],n,p=[0.75,0.25])
})
dc.iloc[-600:,0] += np.linspace(0,50,600)
dc.iloc[-600:,1] += np.linspace(0,8,600)
dc["Normal/Attack"] = make_labels(n,600)
dc.to_csv("data/test_datacenter.csv", index=False)


print("✅ 5 domain datasets generated")
