import subprocess
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_step(command, name):
    print(f"\n🚀 Running {name}...")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"❌ {name} failed.")
        sys.exit(1)

    print(f"✅ {name} completed.")


def run_pipeline():

    # ==========================
    # 1️⃣ Twin Builder
    # ==========================
    run_step(
        "python twin/twin_builder.py",
        "Digital Twin Builder"
    )

    # ==========================
    # 2️⃣ Attack Engine
    # ==========================
    run_step(
        "python attack/attack_engine.py",
        "Attack Engine"
    )

    # ==========================
    # 3️⃣ AI Explainer
    # ==========================
    run_step(
        "python ai/ai_explainer.py",
        "AI Reasoning Engine"
    )

    print("\n🔥 FULL GEN-TWIN PIPELINE COMPLETE")

    run_step(
        "streamlit run ui/app.py",
        "Launching Security Dashboard"
    )


if __name__ == "__main__":
    run_pipeline()
