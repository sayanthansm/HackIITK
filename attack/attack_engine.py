import pandas as pd
import json

class AttackEngine:

    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)

    def detect_attack_windows(self):
        # Assume Label column exists
        attacks = self.df[self.df["Label"] == "Attack"]
        return attacks

    def build_attack_chain(self, attack_rows):
        chains = []

        for _, row in attack_rows.iterrows():
            chain = {
                "start_node": "P1",
                "path": ["P1", "P2", "P3"],
                "impact": "Tank Level Increase"
            }
            chains.append(chain)

        return chains

    def save_paths(self, chains):
        with open("data/attack_paths.json", "w") as f:
            json.dump(chains, f, indent=2)
