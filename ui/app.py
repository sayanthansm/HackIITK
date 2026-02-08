import streamlit as st
import json
import os
import sys

# ---------- path setup ----------
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from pyvis.network import Network
from ai.ai_explainer import generate_ai_report

st.set_page_config(page_title="GenTwin Command Center", layout="wide")

# ---------- styling ----------
st.markdown("""
<style>
@keyframes pulseGlow {
  0% { box-shadow: 0 0 8px rgba(59,130,246,0.4); }
  50% { box-shadow: 0 0 22px rgba(59,130,246,0.9); }
  100% { box-shadow: 0 0 8px rgba(59,130,246,0.4); }
}

.hero {
    padding: 28px;
    border-radius: 22px;
    background: linear-gradient(135deg,#020617,#0f172a,#020617);
    border: 1px solid rgba(255,255,255,0.08);
    animation: pulseGlow 3s infinite;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🏭 GenTwin Cyber-Physical Defense Console</h1>
<p>Digital Twin + GenAI Attack Surface Reasoning Engine</p>
</div>
""", unsafe_allow_html=True)

# ---------- header ----------
st.markdown('<div class="big-title">🏭 GenTwin Security Command Center</div>', unsafe_allow_html=True)
st.caption("Detect → Reason → Mitigate using GenAI + Digital Twin")

ATTACK_PATH_FILE = os.path.join(ROOT_DIR, "attack_paths.json")

# ---------- load attack report ----------
@st.cache_data
def load_attack():
    if not os.path.exists(ATTACK_PATH_FILE):
        st.error("attack_paths.json not found — run attack_engine.py first")
        st.stop()

    with open(ATTACK_PATH_FILE) as f:
        return json.load(f)

# ---------- graph builder ----------
def build_graph(chain, compromised):
    net = Network(height="520px", width="100%", bgcolor="#0f172a", font_color="white")

    # chain nodes
    for n in chain:
        net.add_node(n, label=n, color="#2563eb", size=26)

    # chain edges
    for i in range(len(chain)-1):
        net.add_edge(chain[i], chain[i+1])

    # compromised nodes
    for c in compromised:
        net.add_node(c, label=c, color="#ef4444", size=18)
        if chain:
            net.add_edge(chain[-1], c)

    net.save_graph("graph.html")
    return "graph.html"

# ---------- run button ----------
if st.button("🚀 Run Full AI Analysis", use_container_width=True):

    with st.spinner("Running GenTwin reasoning engine..."):
        data = load_attack()
        ai = generate_ai_report(ATTACK_PATH_FILE)

    risk_level = data.get("risk_level", "LOW")
    risk_score = data.get("risk_score", 0)
    chain = data.get("attack_chain", [])
    compromised = data.get("compromised_nodes", [])

    risk_icon = {"LOW":"🟢","MEDIUM":"🟠","HIGH":"🔴"}.get(risk_level, "⚪")

    # ---------- metrics ----------
    c1,c2,c3 = st.columns(3)

    c1.markdown(f"""
    <div class="section-card">
    <h4>Risk Level</h4>
    <h2>{risk_icon} {risk_level}</h2>
    </div>
    """, unsafe_allow_html=True)

    c2.metric("Risk Score", risk_score)
    c3.metric("AI Confidence", ai["confidence"])

    st.divider()

    # ---------- AI narrative ----------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🧠 AI Attack Narrative")
    st.info(ai["ai_explanation"])
    st.markdown('</div>', unsafe_allow_html=True)

    left,right = st.columns(2)

    # ---------- LEFT ----------
    with left:
        st.subheader("🔧 Compromised Components")
        if compromised:
            for c in compromised:
                st.markdown(f'<span class="badge">{c}</span>', unsafe_allow_html=True)
        else:
            st.write("No compromised nodes detected")

        st.subheader("🔗 Attack Chain")
        if chain:
            for s in chain:
                st.markdown(f'<span class="badge">{s}</span>', unsafe_allow_html=True)
        else:
            st.write("No propagation chain derived")

    # ---------- RIGHT ----------
    with right:
        st.subheader("💥 Impact")
        for x in ai["impact_summary"]:
            st.markdown(f'<span class="badge">{x}</span>', unsafe_allow_html=True)

        st.subheader("🛡 Mitigations")
        for x in ai["mitigation_suggestions"]:
            st.markdown(f'<span class="badge">{x}</span>', unsafe_allow_html=True)

    # ---------- gaps ----------
    st.subheader("🕳 Security Gaps")
    for g in ai["discovered_gaps"]:
        st.markdown(f'<span class="badge">{g}</span>', unsafe_allow_html=True)

    st.divider()

    # ---------- graph ----------
    st.subheader("🌐 Digital Twin Attack Propagation Map")
    html_file = build_graph(chain, compromised)

    with open(html_file) as f:
        st.components.v1.html(f.read(), height=540)
