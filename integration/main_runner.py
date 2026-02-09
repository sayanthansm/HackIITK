import os
import sys

# ===== IMPORT YOUR MODULES =====
# Adjust imports if filenames differ

from twin.twin_builder import build_twin_graph
from attack.attack_engine import run_attack_analysis
from ai.ai_explainer import generate_ai_report


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TWIN_OUTPUT = os.path.join(BASE_DIR, "twin_graph.json")
ATTACK_OUTPUT = os.path.join(BASE_DIR, "attack_paths.json")


def run_pipeline(dataset_path: str):
    """
    Full GenTwin pipeline:
    Dataset -> Twin -> Attack -> AI reasoning
    """

    print("\n🚀 Starting GenTwin Pipeline")
    print(f"📂 Dataset: {dataset_path}")

    # =============================
    # 1️⃣ Build Digital Twin
    # =============================
    print("\n🔧 Building Digital Twin...")
    build_twin_graph(dataset_path, TWIN_OUTPUT)

    # =============================
    # 2️⃣ Attack Analyzer
    # =============================
    print("\n⚠️ Running Attack Analysis...")
    run_attack_analysis(
        dataset_path=dataset_path,
        twin_graph_path=TWIN_OUTPUT,
        output_path=ATTACK_OUTPUT
    )

    # =============================
    # 3️⃣ AI Reasoning
    # =============================
    print("\n🤖 Generating AI Explanation...")
    report = generate_ai_report(ATTACK_OUTPUT)

    print("\n✅ Pipeline Completed")
    return report


# ====================================
# CLI USAGE
# ====================================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("\n❌ Usage:")
        print("python main_runner.py <dataset_csv>")
        sys.exit(1)

    dataset = sys.argv[1]
    run_pipeline(dataset)
