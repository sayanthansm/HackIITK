import streamlit as st
import json
import os
import sys
from pyvis.network import Network
import streamlit.components.v1 as components

# ---------------- PATH CONFIGURATION ----------------
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

try:
    from ai.ai_explainer import generate_ai_report as real_generate_ai_report
except ImportError:
    real_generate_ai_report = None


# ---------------- SAFE AI WRAPPER ----------------
def mock_ai_report():
    return {
        "confidence": 0.5,
        "ai_explanation": "AI module unavailable — fallback mode active.",
        "impact_summary": ["Impact data unavailable"],
        "mitigation_suggestions": ["Mitigation data unavailable"],
        "discovered_gaps": ["Gap analysis unavailable"]
    }


def generate_ai_safe(path):
    if real_generate_ai_report and path and os.path.exists(path):
        try:
            return real_generate_ai_report(path)
        except Exception:
            st.warning("AI module error — using fallback")
    return mock_ai_report()


ATTACK_PATH_FILE = os.path.join(ROOT_DIR, "attack_paths.json")


# ---------------- LOAD REAL ENGINE OUTPUT ----------------
@st.cache_data
def load_attack():
    if not os.path.exists(ATTACK_PATH_FILE):
        st.error("attack_paths.json not found — run attack_engine.py first")
        st.stop()

    with open(ATTACK_PATH_FILE) as f:
        return json.load(f)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenTwin Security Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b1220, #0f172a);
    color: #e2e8f0;
}

.glass-card {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 18px;
    color: #60a5fa;
    border-bottom: 1px solid rgba(96,165,250,0.25);
    padding-bottom: 10px;
}

ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

li {
    font-size: 16px;
    margin-bottom: 10px;
    color: #d1d5db;
}

li::before { content: ""; }

.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: #3b82f6;
}

.metric-label {
    font-size: 14px;
    text-transform: uppercase;
    opacity: 0.8;
}

.stButton>button {
    background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
    font-size: 18px !important;
    padding: 12px !important;
    border-radius: 12px !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GRAPH ----------------
def build_graph(chain, compromised):
    net = Network(height="560px", width="100%", bgcolor="#0b1220", font_color="white")

    for n in chain:
        net.add_node(n, label=n, color="#3b82f6", size=28)

    for i in range(len(chain)-1):
        net.add_edge(chain[i], chain[i+1])

    for c in compromised:
        net.add_node(c, label=c, color="#ef4444", size=40, shape="diamond")
        if chain:
            net.add_edge(chain[-1], c, dashes=True)

    path = "graph_output.html"
    net.save_graph(path)
    return path


# ---------------- HEADER ----------------
st.title("🏭 GenTwin Security Dashboard")
st.caption("Digital Twin + Generative AI Attack Surface Analysis")
st.divider()

# ---------------- RUN ----------------
if st.button("🚀 Run System Analysis", use_container_width=True):

    # ✅ REAL DATA — NOT MOCK
    data = load_attack()
    ai = generate_ai_safe(ATTACK_PATH_FILE)

    risk_level = data["risk_level"]
    risk_score = data["risk_score"]
    attack_chain = data["attack_chain"]
    compromised_nodes = data["compromised_nodes"]

    # -------- Metrics --------
    c1, c2, c3 = st.columns(3)

    c1.markdown(
        f'<div class="glass-card"><div class="metric-label">Risk Level</div>'
        f'<div class="metric-value">{risk_level}</div></div>',
        unsafe_allow_html=True
    )

    c2.markdown(
        f'<div class="glass-card"><div class="metric-label">Risk Score</div>'
        f'<div class="metric-value">{risk_score}/100</div></div>',
        unsafe_allow_html=True
    )

    c3.markdown(
        f'<div class="glass-card"><div class="metric-label">AI Confidence</div>'
        f'<div class="metric-value">{ai["confidence"]}</div></div>',
        unsafe_allow_html=True
    )

    # -------- AI Summary --------
    st.markdown(f'''
    <div class="glass-card">
        <div class="card-title">AI Reasoning Summary</div>
        <div style="font-size:16px">{ai["ai_explanation"]}</div>
    </div>
    ''', unsafe_allow_html=True)

    # -------- Grid --------
    col_left, col_right = st.columns(2)

    with col_left:
        comp_html = "".join([f"<li>{x}</li>" for x in compromised_nodes])
        st.markdown(
            f'<div class="glass-card"><div class="card-title">Compromised Components</div>'
            f'<ul>{comp_html}</ul></div>',
            unsafe_allow_html=True
        )

        chain_html = "".join([f"<li>{x}</li>" for x in attack_chain])
        st.markdown(
            f'<div class="glass-card"><div class="card-title">Attack Chain</div>'
            f'<ul>{chain_html}</ul></div>',
            unsafe_allow_html=True
        )

    with col_right:
        impact_html = "".join([f"<li>{x}</li>" for x in ai["impact_summary"]])
        st.markdown(
            f'<div class="glass-card"><div class="card-title">Impact</div>'
            f'<ul>{impact_html}</ul></div>',
            unsafe_allow_html=True
        )

        mit_html = "".join([f"<li>{x}</li>" for x in ai["mitigation_suggestions"]])
        st.markdown(
            f'<div class="glass-card"><div class="card-title">Mitigations</div>'
            f'<ul>{mit_html}</ul></div>',
            unsafe_allow_html=True
        )

    # -------- Gaps --------
    gaps_html = "".join([f"<li>{x}</li>" for x in ai["discovered_gaps"]])
    st.markdown(
        f'<div class="glass-card"><div class="card-title">Security Gaps</div>'
        f'<ul>{gaps_html}</ul></div>',
        unsafe_allow_html=True
    )

    # -------- Graph --------
    st.markdown('<div class="glass-card"><div class="card-title">Attack Graph</div>',
                unsafe_allow_html=True)

    html_path = build_graph(attack_chain, compromised_nodes)
    with open(html_path, "r", encoding="utf-8") as f:
        components.html(f.read(), height=620)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("System Ready. Click Run System Analysis.")

st.divider()
st.caption("GenTwin v1.0 — Security Dashboard")
