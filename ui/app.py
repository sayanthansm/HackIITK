import streamlit as st
import json
import os
import sys

# add repo root to python path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from pyvis.network import Network
from ai.ai_explainer import generate_ai_report

st.set_page_config(page_title="GenTwin Command Center", layout="wide")

# ---------- styling ----------
st.markdown("""
<style>
.big-title {
    font-size: 44px;
    font-weight: 900;
    background: linear-gradient(90deg,#00e5ff,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2em;
}

.section-card {
    background: linear-gradient(145deg,#0b1220,#111827);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

.glow-high {
    box-shadow: 0 0 18px rgba(239,68,68,0.6);
    border-radius: 50%;
}

.badge {
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    font-size:14px;
    font-weight:600;
    background:#1f2937;
    border:1px solid rgba(255,255,255,0.1);
    margin-right:6px;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="big-title">🏭 GenTwin Security Command Center</div>', unsafe_allow_html=True)
st.caption("Detect → Reason → Mitigate using GenAI + Digital Twin")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ATTACK_PATH_FILE = os.path.join(BASE_DIR, "attack_paths.json")

# ---------- load ----------
@st.cache_data
def load_attack():
    if not os.path.exists(ATTACK_PATH_FILE):
        st.error("attack_paths.json not found — run attack_engine.py first")
        st.stop()

    with open(ATTACK_PATH_FILE) as f:
        return json.load(f)

# ---------- graph builder ----------
def build_graph(stages, compromised):
    net = Network(height="500px", width="100%", bgcolor="#0f172a", font_color="white")

    for s in stages:
        net.add_node(s, label=s, color="#2563eb", size=25)

    for i in range(len(stages)-1):
        net.add_edge(stages[i], stages[i+1])

    for c in compromised:
        net.add_node(c, label=c, color="#ef4444", size=18)
        net.add_edge(stages[-1], c)

    net.save_graph("graph.html")
    return "graph.html"

# ---------- run button ----------
if st.button("🚀 Run Full AI Analysis", use_container_width=True):

    with st.spinner("Running GenTwin reasoning engine..."):
        data = load_attack()
        ai = generate_ai_report(ATTACK_PATH_FILE)

    # ---------- metrics ----------
    c1,c2,c3 = st.columns(3)

    risk_color = {"LOW":"🟢","MEDIUM":"🟠","HIGH":"🔴"}[data["risk_level"]]

    c1.markdown(f"""
    <div class="section-card">
    <h4>Risk Level</h4>
    <h2>{risk_color} {data['risk_level']}</h2>
    </div>
    """, unsafe_allow_html=True)

    c2.metric("Risk Score", data["risk_score"])
    c3.metric("AI Confidence", ai["confidence"])

    st.divider()

    # ---------- AI narrative ----------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🧠 AI Attack Narrative")
    st.info(ai["ai_explanation"])
    st.markdown('</div>', unsafe_allow_html=True)

    left,right = st.columns(2)

    # ---------- LEFT COLUMN ----------
    with left:
        st.subheader("🔧 Compromised Components")
        for c in data["compromised_nodes"]:
            st.markdown(f'<span class="badge">{c}</span>', unsafe_allow_html=True)


        st.subheader("🏭 Affected Stages")
        for s in data["attack_stages"]:
            st.markdown(f'<span class="badge">{s}</span>', unsafe_allow_html=True)

    # ---------- RIGHT COLUMN ----------
    with right:
        st.subheader("💥 Impact")
        for x in ai["impact_summary"]:
            st.markdown(f'<span class="badge">{x}</span>', unsafe_allow_html=True)

        st.subheader("🛡 Mitigations")
        for x in ai["mitigation_suggestions"]:
            st.markdown(f'<span class="badge">{x}</span>', unsafe_allow_html=True)

    st.subheader("🕳 Security Gaps")
    for g in ai["discovered_gaps"]:
        st.markdown(f'<span class="badge">{g}</span>', unsafe_allow_html=True)

    st.divider()

    # ---------- graph ----------
    st.markdown("## 🌐 Digital Twin Attack Propagation Map")
    st.caption("Graph-based cyber-physical compromise spread")


    html_file = build_graph(data["attack_stages"], data["compromised_nodes"])
    with open(html_file) as f:
        st.components.v1.html(f.read(), height=520)
