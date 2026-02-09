class RiskEngine:

    def compute_risk(self, chain):

        base = len(chain["path"]) * 8

        if chain.get("detection_method") == "GAN_reconstruction_error":
            base += 15

        if "Tank" in chain.get("impact", ""):
            base += 20

        return min(base, 100)
