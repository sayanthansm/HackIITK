class RiskEngine:

    def compute_risk(self, chain):
        # SIMPLE FAST SCORING (Hackathon-friendly)
        base = len(chain["path"]) * 10

        if "Tank" in chain["impact"]:
            base += 20

        return min(base, 100)
