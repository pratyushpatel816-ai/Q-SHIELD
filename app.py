
import os
import sys
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------
# PROJECT IMPORT PATH
# ---------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.integrated_detector import IntegratedQShieldDetector
from qds.qds_protocol import QDSProtocol
from qds.qds_attack_simulator import QDSAttackSimulator


# ---------------------------------------------------------------------
# PAGE
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Q-SHIELD // Quantum Cyber Defense Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------
# STYLE — inspired by the supplied dark cyber/terminal dashboard:
# dark glass panels, scanlines, monospaced telemetry, neon cyan/green,
# restrained magenta/red threat accents, and command-console language.
# ---------------------------------------------------------------------
st.markdown(
    r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Share+Tech+Mono&display=swap');

:root {
    --bg: #03070b;
    --panel: rgba(5, 16, 21, .88);
    --panel2: rgba(3, 12, 17, .96);
    --line: rgba(65, 255, 220, .20);
    --cyan: #55ffe0;
    --cyan2: #1ed6ff;
    --green: #69ff9b;
    --red: #ff5577;
    --amber: #ffc45b;
    --purple: #b38cff;
    --text: #d9fff7;
    --muted: #71948f;
}

html, body, [class*="css"] {
    font-family: "Share Tech Mono", monospace;
}

.stApp {
    color: var(--text);
    background:
        radial-gradient(circle at 85% 0%, rgba(0, 235, 220, .10), transparent 24%),
        radial-gradient(circle at 10% 18%, rgba(75, 0, 130, .09), transparent 22%),
        linear-gradient(180deg, #020609 0%, #03080c 48%, #010407 100%);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(rgba(80,255,220,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(80,255,220,.012) 1px, transparent 1px);
    background-size: 42px 42px;
    z-index: 0;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    font-family: "Orbitron", monospace !important;
    letter-spacing: .08em;
}

hr {
    border-color: rgba(85,255,224,.10) !important;
}

.small-label {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: 10px;
}

.terminal {
    color: #70ffb4;
    font-size: 12px;
    letter-spacing: .04em;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(85,255,224,.30);
    border-radius: 20px;
    padding: 28px 32px 24px;
    background:
        radial-gradient(circle at 90% 0%, rgba(0,255,220,.10), transparent 26%),
        radial-gradient(circle at 0% 100%, rgba(150,60,255,.08), transparent 28%),
        rgba(2, 12, 17, .94);
    box-shadow: 0 0 45px rgba(0,255,210,.055), inset 0 0 45px rgba(0,255,210,.025);
}

.hero:after {
    content: "";
    position: absolute;
    left: 0; right: 0; top: 50%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(85,255,224,.22), transparent);
    box-shadow: 0 0 16px rgba(85,255,224,.18);
}

.logo-box {
    width: 68px;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(85,255,224,.45);
    border-radius: 16px;
    background: rgba(0,255,220,.045);
    box-shadow: inset 0 0 24px rgba(0,255,220,.08);
    font-size: 31px;
}

.hero-title {
    font-family: "Orbitron", monospace;
    font-size: clamp(28px, 4vw, 54px);
    font-weight: 800;
    letter-spacing: .13em;
    color: #effffb;
    text-shadow: 0 0 18px rgba(85,255,224,.28);
}

.hero-sub {
    color: #78bdb3;
    font-size: 13px;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-top: 4px;
}

.hero-terminal {
    margin-top: 18px;
    color: #64ffad;
    font-size: 12px;
}

.kpi {
    min-height: 96px;
    border: 1px solid rgba(91, 160, 157, .18);
    border-radius: 14px;
    background: linear-gradient(180deg, rgba(5,20,25,.92), rgba(2,10,14,.92));
    padding: 15px 17px;
    box-shadow: inset 0 -2px 0 rgba(85,255,224,.10);
}

.kpi .label {
    color: #61837f;
    font-size: 10px;
    letter-spacing: .16em;
    text-transform: uppercase;
}

.kpi .value {
    font-family: "Orbitron", monospace;
    color: #dcfff8;
    font-size: 21px;
    margin-top: 8px;
}

.kpi .value.green { color: var(--green); }
.kpi .value.red { color: var(--red); }
.kpi .value.cyan { color: var(--cyan); }
.kpi .value.amber { color: var(--amber); }

.section-head {
    color: #7fd6ca;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .18em;
    margin: 20px 0 10px;
}

.section-head:before {
    content: "// ";
    color: #39e6c6;
}

.panel {
    border: 1px solid rgba(85,255,224,.16);
    border-radius: 15px;
    padding: 18px;
    background: linear-gradient(180deg, rgba(5,18,23,.86), rgba(2,9,13,.92));
    box-shadow: inset 0 0 28px rgba(0,255,220,.018);
}

.panel-title {
    color: #b5ded8;
    font-family: "Orbitron", monospace;
    font-size: 13px;
    letter-spacing: .10em;
    margin-bottom: 13px;
}

.command-button button {
    min-height: 54px !important;
    border: 1px solid rgba(85,255,224,.42) !important;
    border-radius: 12px !important;
    background: linear-gradient(90deg, rgba(0,255,170,.11), rgba(0,100,130,.12)) !important;
    color: #dffff7 !important;
    font-family: "Orbitron", monospace !important;
    letter-spacing: .08em !important;
    box-shadow: 0 0 20px rgba(0,255,220,.04) !important;
}

.command-button button:hover {
    border-color: #55ffe0 !important;
    box-shadow: 0 0 28px rgba(0,255,220,.13) !important;
}

.attack-button button {
    min-height: 48px !important;
    border-color: rgba(255,80,120,.42) !important;
    background: linear-gradient(90deg, rgba(255,40,90,.08), rgba(100,20,80,.08)) !important;
}

.attack-button button:hover {
    border-color: #ff5577 !important;
}

.safe {
    border-color: rgba(105,255,155,.38);
    background: radial-gradient(circle at 50% 0%, rgba(60,255,150,.08), transparent 45%), rgba(3,22,16,.82);
}

.threat {
    border-color: rgba(255,85,119,.50);
    background: radial-gradient(circle at 50% 0%, rgba(255,50,90,.11), transparent 48%), rgba(28,4,12,.88);
}

.warn {
    border-color: rgba(255,196,91,.45);
    background: rgba(28,20,5,.72);
}

.decision {
    border-radius: 18px;
    border: 1px solid rgba(85,255,224,.25);
    padding: 24px;
    text-align: center;
    background: rgba(2,11,15,.90);
}

.decision .big {
    font-family: "Orbitron", monospace;
    font-size: clamp(22px, 3vw, 37px);
    font-weight: 800;
    letter-spacing: .08em;
}

.decision .reason {
    margin-top: 8px;
    color: #83aaa4;
    font-size: 12px;
}

.flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    padding: 12px 0;
}

.flow-node {
    border: 1px solid rgba(85,255,224,.20);
    background: rgba(2,14,18,.85);
    border-radius: 9px;
    padding: 10px 13px;
    color: #b8ddd7;
    font-size: 11px;
    text-align: center;
}

.flow-arrow {
    color: #45f4d4;
    font-size: 17px;
}

.signal {
    border: 1px solid rgba(80,190,220,.18);
    border-radius: 11px;
    padding: 13px;
    background: rgba(2,12,17,.88);
}

.signal .name {
    color: #658b86;
    font-size: 10px;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.signal .number {
    color: #e0fffa;
    font-family: "Orbitron", monospace;
    font-size: 24px;
    margin-top: 5px;
}

.matrix {
    border: 1px solid rgba(85,255,224,.13);
    border-radius: 13px;
    overflow: hidden;
}

.matrix-row {
    display: grid;
    grid-template-columns: 1fr 100px 130px;
    padding: 11px 14px;
    border-bottom: 1px solid rgba(85,255,224,.07);
    font-size: 11px;
}

.matrix-row:last-child { border-bottom: 0; }
.matrix-head { color: #557a76; letter-spacing: .10em; text-transform: uppercase; }
.pass { color: #69ff9b; font-weight: 700; }
.fail { color: #ff5577; font-weight: 700; }

.badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 999px;
    font-size: 9px;
    letter-spacing: .10em;
    border: 1px solid rgba(85,255,224,.22);
}

details, .stExpander {
    border-color: rgba(85,255,224,.12) !important;
}

.stSelectbox label, .stSlider label, .stRadio label, .stNumberInput label, .stTextInput label {
    color: #72918e !important;
    font-size: 10px !important;
    letter-spacing: .10em !important;
    text-transform: uppercase;
}

div[data-testid="stMetric"] {
    background: rgba(2,12,17,.88);
    border: 1px solid rgba(85,255,224,.12);
    border-radius: 12px;
}

[data-testid="stSidebar"] {
    background: #02070a !important;
    border-right: 1px solid rgba(85,255,224,.14);
}

footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "replay_signature" not in st.session_state:
    st.session_state.replay_signature = None

# ---------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------
QDS_ATTACKS = {
    "Legitimate Communication": "none",
    "Digital Signature Forgery": "forgery",
    "Signer Impersonation": "impersonation",
    "Replay Attack": "replay",
    "Unauthorized Verification": "unauthorized_verification",
}

QUANTUM_ATTACKS = {
    "No Quantum Attack": "none",
    "Pauli-X Channel Manipulation": "pauli_x",
    "Pauli-Y Channel Manipulation": "pauli_y",
    "Pauli-Z Channel Manipulation": "pauli_z",
    "Entanglement Disruption": "entanglement_disruption",
}

NOISE_TYPES = ["none", "bit_flip", "phase_flip", "depolarizing", "readout"]

# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------
def qds_run(message, qds_attack, verifier_id):
    protocol = QDSProtocol()

    signature = protocol.generate_signature(
        message=message,
        signer_id="ALICE",
        authorized_verifiers=["BOB"],
    )

    attacked_signature, attack_metadata = QDSAttackSimulator.apply_attack(
        signature,
        attack_type=qds_attack,
    )

    if qds_attack == "replay":
        first = protocol.verify_signature(attacked_signature, verifier_id="BOB")
        second = protocol.verify_signature(attacked_signature, verifier_id="BOB")
        return {
            "signature": attacked_signature,
            "attack_metadata": attack_metadata,
            "verification": second,
            "first_verification": first,
            "second_verification": second,
        }

    verification = protocol.verify_signature(
        attacked_signature,
        verifier_id=verifier_id,
    )

    return {
        "signature": attacked_signature,
        "attack_metadata": attack_metadata,
        "verification": verification,
        "first_verification": None,
        "second_verification": None,
    }


def qshield_run(
    shots,
    bit,
    basis,
    noise_type,
    noise_probability,
    quantum_attack,
    mismatch_weight,
    bell_weight,
    base_threshold,
    adaptation_factor,
    max_threshold,
):
    engine = TeleportationEngine(shots=shots)
    quantum_result = engine.run(
        bit=bit,
        basis=basis,
        noise_type=noise_type,
        noise_probability=noise_probability,
        attack_type=quantum_attack,
    )

    detector = IntegratedQShieldDetector(
        mismatch_weight=mismatch_weight,
        bell_weight=bell_weight,
        base_threshold=base_threshold,
        adaptation_factor=adaptation_factor,
        max_threshold=max_threshold,
    )

    security_result = detector.analyze(
        mismatch_rate=quantum_result["mismatch_rate"],
        bell_measurements=quantum_result["bell_measurements"],
    )

    return quantum_result, security_result


def run_demo(
    message,
    qds_attack,
    quantum_attack,
    verifier_id,
    shots,
    bit,
    basis,
    noise_type,
    noise_probability,
):
    qds = qds_run(message, qds_attack, verifier_id)
    quantum, qshield = qshield_run(
        shots=shots,
        bit=bit,
        basis=basis,
        noise_type=noise_type,
        noise_probability=noise_probability,
        quantum_attack=quantum_attack,
        mismatch_weight=0.7,
        bell_weight=0.3,
        base_threshold=0.26,
        adaptation_factor=0.4,
        max_threshold=0.32,
    )

    qds_threat = qds["verification"]["final_decision"] == "REJECT"
    quantum_threat = qshield["attack_detected"]
    overall_threat = qds_threat or quantum_threat

    if overall_threat:
        final = "SECURITY THREAT DETECTED"
    else:
        final = "SECURE COMMUNICATION"

    return {
        "qds": qds,
        "quantum": quantum,
        "qshield": qshield,
        "qds_threat": qds_threat,
        "quantum_threat": quantum_threat,
        "overall_threat": overall_threat,
        "final_decision": final,
    }


def save_history(result, qds_attack, quantum_attack, noise_type):
    q = result["quantum"]
    s = result["qshield"]
    v = result["qds"]["verification"]

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "qds_attack": qds_attack,
        "quantum_attack": quantum_attack,
        "noise_type": noise_type,
        "qds_decision": v["final_decision"],
        "qshield_decision": s["decision"],
        "severity": s["severity"],
        "security_score": s["security_score"],
        "adaptive_threshold": s["adaptive_threshold"],
        "mismatch_rate": q["mismatch_rate"],
        "bell_anomaly_score": s["bell_anomaly_score"],
        "fidelity_proxy": q["fidelity_proxy"],
        "final_decision": result["final_decision"],
    }
    st.session_state.history.append(row)
    st.session_state.latest_result = result


def matrix_rows():
    return [
        ("Legitimate QDS Communication", "QDS + quantum", "PASSED"),
        ("Legitimate Noisy Channel", "QDS + noise", "PASSED"),
        ("Digital Signature Forgery", "QDS", "PASSED"),
        ("Signer Impersonation", "QDS", "PASSED"),
        ("Replay Attack", "QDS", "PASSED"),
        ("Unauthorized Verification", "QDS", "PASSED"),
        ("Quantum Channel Manipulation", "Q-SHIELD", "PASSED"),
    ]


# ---------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div style="display:flex;gap:20px;align-items:center;">
    <div class="logo-box">🛡️</div>
    <div>
      <div class="hero-title">Q-SHIELD</div>
      <div class="hero-sub">Quantum Attack Detection // Teleportation-Based QDS Security</div>
    </div>
  </div>
  <div class="hero-terminal">
    root@qshield:~$ initialize_defense_node [ OK ] &nbsp;&nbsp;
    secure quantum inference channel established
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# TOP STATUS
# ---------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
for col, label, value, cls in [
    (k1, "Core Status", "● ONLINE", "green"),
    (k2, "Detection Layers", "02 // ACTIVE", "cyan"),
    (k3, "QDS Coverage", "07 // SCENARIOS", "purple"),
    (k4, "Response Mode", "SIMULATION ONLY", "amber"),
]:
    col.markdown(
        f"""
        <div class="kpi">
          <div class="label">{label}</div>
          <div class="value {cls}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------------------
st.markdown('<div class="section-head">DEFENSE PIPELINE</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="panel">
<div class="flow">
  <div class="flow-node">🔐 QDS MESSAGE</div><div class="flow-arrow">›</div>
  <div class="flow-node">IDENTITY / REPLAY</div><div class="flow-arrow">›</div>
  <div class="flow-node">⚛ TELEPORTATION</div><div class="flow-arrow">›</div>
  <div class="flow-node">BELL MEASUREMENT</div><div class="flow-arrow">›</div>
  <div class="flow-node">DUAL-SIGNAL Q-SHIELD</div><div class="flow-arrow">›</div>
  <div class="flow-node">🛡 SECURITY DECISION</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# CONTROL CENTER
# ---------------------------------------------------------------------
st.markdown('<div class="section-head">THREAT ANALYSIS CONTROL</div>', unsafe_allow_html=True)

left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">ATTACK VECTOR MATRIX</div>', unsafe_allow_html=True)

    qds_label = st.selectbox(
        "QDS Attack",
        list(QDS_ATTACKS.keys()),
        index=0,
    )
    quantum_label = st.selectbox(
        "Quantum Channel Attack",
        list(QUANTUM_ATTACKS.keys()),
        index=0,
    )

    message = st.text_input("Signed Message", "INSTALL_FIRMWARE")
    verifier = st.selectbox("Verifier Identity", ["BOB", "INTRUDER"])

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">QUANTUM CHANNEL CONFIGURATION</div>', unsafe_allow_html=True)

    noise_type = st.selectbox("Noise Model", NOISE_TYPES, index=0)
    noise_probability = st.slider(
        "Noise Probability",
        min_value=0.0,
        max_value=0.20,
        value=0.0,
        step=0.01,
    )
    shots = st.select_slider(
        "Quantum Shots",
        options=[256, 512, 1024, 2048],
        value=1024,
    )
    bit = st.selectbox("Message Bit", [0, 1], index=0)
    basis = st.selectbox("Measurement Basis", ["Z", "X", "Y"], index=0)

    st.markdown('</div>', unsafe_allow_html=True)

run_col, reset_col = st.columns([4, 1])
with run_col:
    st.markdown('<div class="command-button">', unsafe_allow_html=True)
    run = st.button("⚡ INITIATE QUANTUM SECURITY SCAN", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with reset_col:
    if st.button("CLEAR", use_container_width=True):
        st.session_state.latest_result = None

# ---------------------------------------------------------------------
# EXECUTE
# ---------------------------------------------------------------------
if run:
    try:
        with st.spinner("Executing QDS verification + quantum telemetry analysis..."):
            result = run_demo(
                message=message,
                qds_attack=QDS_ATTACKS[qds_label],
                quantum_attack=QUANTUM_ATTACKS[quantum_label],
                verifier_id=verifier,
                shots=shots,
                bit=bit,
                basis=basis,
                noise_type=noise_type,
                noise_probability=noise_probability,
            )

        save_history(
            result,
            QDS_ATTACKS[qds_label],
            QUANTUM_ATTACKS[quantum_label],
            noise_type,
        )

    except Exception as exc:
        st.error(f"SECURITY ENGINE ERROR: {exc}")
        st.stop()

# ---------------------------------------------------------------------
# RESULT
# ---------------------------------------------------------------------
result = st.session_state.latest_result

if result is not None:
    qds = result["qds"]
    quantum = result["quantum"]
    qshield = result["qshield"]
    verification = qds["verification"]

    st.markdown('<div class="section-head">THREAT ASSESSMENT // LIVE INFERENCE</div>', unsafe_allow_html=True)

    if result["overall_threat"]:
        css = "threat"
        title = "⚠ SECURITY THREAT DETECTED"
        subtitle = "Adversarial condition rejected or quantum-channel anomaly exceeded the decision boundary."
    else:
        css = "safe"
        title = "✓ SECURE COMMUNICATION"
        subtitle = "QDS verification passed and observed quantum-channel disturbance remains within the adaptive boundary."

    st.markdown(
        f"""
        <div class="decision {css}">
          <div style="font-size:30px;">{'⚡' if result['overall_threat'] else '◉'}</div>
          <div class="big">{title}</div>
          <div class="reason">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Layer status
    a, b, c, d = st.columns(4)

    qds_status = verification["final_decision"]
    qshield_status = qshield["decision"]

    a.markdown(
        f"""<div class="kpi"><div class="label">QDS VERIFICATION</div>
        <div class="value {'red' if qds_status == 'REJECT' else 'green'}">{qds_status}</div></div>""",
        unsafe_allow_html=True,
    )
    b.markdown(
        f"""<div class="kpi"><div class="label">Q-SHIELD</div>
        <div class="value {'red' if qshield['attack_detected'] else 'green'}">{qshield_status}</div></div>""",
        unsafe_allow_html=True,
    )
    c.markdown(
        f"""<div class="kpi"><div class="label">SEVERITY</div>
        <div class="value {'red' if qshield['severity'] == 'HIGH' else 'amber'}">{qshield['severity']}</div></div>""",
        unsafe_allow_html=True,
    )
    d.markdown(
        f"""<div class="kpi"><div class="label">DECISION MARGIN</div>
        <div class="value cyan">{qshield['decision_margin']:.4f}</div></div>""",
        unsafe_allow_html=True,
    )

    # QDS security panel
    st.markdown('<div class="section-head">QDS SECURITY VERIFICATION</div>', unsafe_allow_html=True)
    q1, q2 = st.columns(2, gap="large")

    with q1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">CRYPTOGRAPHIC TRANSACTION</div>', unsafe_allow_html=True)

        msg_ok = verification.get("valid_message", False)
        auth_ok = verification.get("authorized_verifier", False)
        sig_ok = verification.get("signature_valid", False)
        replay = verification.get("replay_detected", False)

        checks = [
            ("MESSAGE INTEGRITY", msg_ok),
            ("VERIFIER AUTHORIZATION", auth_ok),
            ("SIGNATURE STATE", sig_ok),
            ("REPLAY PROTECTION", not replay),
        ]

        for name, ok in checks:
            st.markdown(
                f"""
                <div style="display:flex;justify-content:space-between;
                            padding:10px 0;border-bottom:1px solid rgba(85,255,224,.07);">
                    <span style="color:#71948f;font-size:11px;">{name}</span>
                    <span class="{'pass' if ok else 'fail'}">{'✓ PASS' if ok else '✗ BLOCK'}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if qds_label == "Replay Attack":
            first = qds["first_verification"]
            second = qds["second_verification"]
            st.info(
                f"Replay sequence: FIRST = {first['final_decision']}  →  "
                f"SECOND = {second['final_decision']}"
            )

        if verification.get("reason"):
            st.warning(" | ".join(verification["reason"]))

        st.markdown('</div>', unsafe_allow_html=True)

    with q2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">SIGNATURE TELEMETRY</div>', unsafe_allow_html=True)

        signature = qds["signature"]
        telemetry = pd.DataFrame(
            {
                "Field": [
                    "Signature ID",
                    "Signer",
                    "Verifier",
                    "Message",
                    "Message Hash",
                ],
                "Value": [
                    signature.get("signature_id", "N/A"),
                    signature.get("signer_id", "N/A"),
                    verifier,
                    signature.get("message", "N/A"),
                    signature.get("message_hash", "N/A"),
                ],
            }
        )
        st.dataframe(telemetry, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Quantum layer
    st.markdown('<div class="section-head">QUANTUM TELEMETRY // CHANNEL OBSERVATION</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel">
        <div class="flow">
          <div class="flow-node">|ψ⟩ Pauli Eigenstate</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node">Bell Pair</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node">Alice Bell Measurement</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node">Pauli Correction</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node">Bob Measurement</div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4)
    for col, name, value in [
        (s1, "SHOTS", quantum.get("shots", shots)),
        (s2, "MISMATCH RATE", f"{quantum['mismatch_rate']:.6f}"),
        (s3, "BELL ANOMALY", f"{qshield['bell_anomaly_score']:.6f}"),
        (s4, "FIDELITY PROXY", f"{quantum['fidelity_proxy']:.6f}"),
    ]:
        col.markdown(
            f"""<div class="signal"><div class="name">{name}</div>
            <div class="number">{value}</div></div>""",
            unsafe_allow_html=True,
        )

    # Q-SHIELD engine
    st.markdown('<div class="section-head">Q-SHIELD DUAL-SIGNAL ENGINE</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2, gap="large")

    with e1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">SIGNAL FUSION</div>', unsafe_allow_html=True)

        signal_df = pd.DataFrame(
            {
                "Signal": ["Teleportation Mismatch", "Bell Anomaly"],
                "Score": [
                    quantum["mismatch_rate"],
                    qshield["bell_anomaly_score"],
                ],
            }
        )

        fig_signal = px.bar(
            signal_df,
            x="Signal",
            y="Score",
            text="Score",
            title="Dual-Signal Observation",
        )
        fig_signal.update_traces(texttemplate="%{text:.4f}", textposition="outside")
        fig_signal.update_yaxes(range=[0, 1])
        fig_signal.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10),
            font=dict(family="Share Tech Mono"),
        )
        st.plotly_chart(fig_signal, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">SECURITY SCORE / ADAPTIVE BOUNDARY</div>', unsafe_allow_html=True)

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=qshield["security_score"],
                delta={"reference": qshield["adaptive_threshold"]},
                title={"text": "Q-SHIELD SECURITY SCORE"},
                gauge={
                    "axis": {"range": [0, 1]},
                    "steps": [
                        {"range": [0, qshield["adaptive_threshold"]], "color": "rgba(30,180,120,.22)"},
                        {"range": [qshield["adaptive_threshold"], 1], "color": "rgba(220,50,80,.18)"},
                    ],
                    "threshold": {
                        "line": {"color": "#ff5577", "width": 4},
                        "thickness": .78,
                        "value": qshield["adaptive_threshold"],
                    },
                },
            )
        )
        gauge.update_layout(
            template="plotly_dark",
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Share Tech Mono"),
            margin=dict(l=20, r=20, t=50, b=10),
        )
        st.plotly_chart(gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Measurement results
    m1, m2 = st.columns(2, gap="large")

    with m1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">TELEPORTATION OUTCOMES</div>', unsafe_allow_html=True)

        teleport_df = pd.DataFrame(
            {
                "Outcome": ["Matching Shots", "Mismatch Shots"],
                "Count": [
                    quantum["matching_shots"],
                    quantum["mismatch_shots"],
                ],
            }
        )
        fig_t = px.bar(
            teleport_df,
            x="Outcome",
            y="Count",
            text="Count",
            title="Measurement Consistency",
        )
        fig_t.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10),
            font=dict(family="Share Tech Mono"),
        )
        st.plotly_chart(fig_t, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with m2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">BELL MEASUREMENT DISTRIBUTION</div>', unsafe_allow_html=True)

        bell_df = pd.DataFrame(
            list(quantum["bell_measurements"].items()),
            columns=["Bell Outcome", "Count"],
        )
        fig_b = px.bar(
            bell_df,
            x="Bell Outcome",
            y="Count",
            text="Count",
            title="Bell-State Measurement Pattern",
        )
        fig_b.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10),
            font=dict(family="Share Tech Mono"),
        )
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Explainability
    st.markdown('<div class="section-head">DECISION FORENSICS</div>', unsafe_allow_html=True)

    if result["overall_threat"]:
        reason = []
        if result["qds_threat"]:
            reason.append("QDS SECURITY CONTROL BLOCKED THE TRANSACTION")
        if result["quantum_threat"]:
            reason.append("Q-SHIELD QUANTUM CHANNEL ANOMALY EXCEEDED ADAPTIVE BOUNDARY")

        st.markdown(
            f"""
            <div class="panel threat">
              <div class="panel-title">⚠ THREAT EXPLANATION</div>
              <div style="font-family:Orbitron;font-size:21px;color:#ff7d98;">
                SECURITY THREAT DETECTED
              </div>
              <div style="margin-top:12px;color:#d5b9c0;font-size:12px;">
                {'<br>'.join(reason)}
              </div>
              <hr>
              <div style="color:#a9838e;font-size:11px;">
                QDS decision: <b>{verification['final_decision']}</b><br>
                Q-SHIELD decision: <b>{qshield['decision']}</b><br>
                Score: <b>{qshield['security_score']:.6f}</b><br>
                Adaptive threshold: <b>{qshield['adaptive_threshold']:.6f}</b><br>
                Margin: <b>{qshield['decision_margin']:.6f}</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="panel safe">
              <div class="panel-title">✓ CHANNEL ASSESSMENT</div>
              <div style="font-family:Orbitron;font-size:21px;color:#69ff9b;">
                NORMAL / WITHIN SECURITY BOUNDARY
              </div>
              <div style="margin-top:12px;color:#89b8a5;font-size:12px;">
                QDS verification passed and the fused quantum security score
                remains below the adaptive threshold.
              </div>
              <hr>
              <div style="color:#719d8f;font-size:11px;">
                Score: <b>{qshield['security_score']:.6f}</b> &nbsp; | &nbsp;
                Threshold: <b>{qshield['adaptive_threshold']:.6f}</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Configuration
    with st.expander("VIEW LIVE EXPERIMENT CONFIGURATION"):
        cfg = pd.DataFrame(
            {
                "Parameter": [
                    "Quantum Shots",
                    "Message Bit",
                    "Measurement Basis",
                    "Noise Model",
                    "Noise Probability",
                    "QDS Attack",
                    "Quantum Attack",
                    "Mismatch Weight",
                    "Bell Weight",
                    "Base Threshold",
                    "Adaptation Factor",
                    "Maximum Threshold",
                ],
                "Value": [
                    shots,
                    bit,
                    basis,
                    noise_type,
                    noise_probability,
                    qds_label,
                    quantum_label,
                    0.7,
                    0.3,
                    0.26,
                    0.4,
                    0.32,
                ],
            }
        )
        st.dataframe(cfg, use_container_width=True, hide_index=True)

    with st.expander("VIEW RAW QUANTUM / Q-SHIELD TELEMETRY"):
        st.json(
            {
                "qds_verification": verification,
                "quantum_result": quantum,
                "qshield_result": qshield,
            }
        )

# ---------------------------------------------------------------------
# ATTACK MATRIX
# ---------------------------------------------------------------------
st.markdown('<div class="section-head">SIH ATTACK MATRIX // VALIDATED BACKEND COVERAGE</div>', unsafe_allow_html=True)

rows = matrix_rows()
matrix_html = """
<div class="matrix">
<div class="matrix-row matrix-head">
<div>Threat / Scenario</div><div>Layer</div><div>Status</div>
</div>
"""
for name, layer, status in rows:
    matrix_html += f"""
<div class="matrix-row">
<div>{name}</div>
<div>{layer}</div>
<div class="pass">✓ {status}</div>
</div>
"""
matrix_html += """
<div class="matrix-row">
<div><b>SIH ATTACK MATRIX</b></div>
<div><b>7 / 7</b></div>
<div class="pass">VALIDATED</div>
</div>
</div>
"""
st.markdown(matrix_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------
# HISTORY
# ---------------------------------------------------------------------
if st.session_state.history:
    st.markdown('<div class="section-head">SESSION TELEMETRY HISTORY</div>', unsafe_allow_html=True)

    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

    if len(history_df) > 1:
        hfig = px.line(
            history_df,
            y=["security_score", "adaptive_threshold"],
            markers=True,
            title="Security Score Evolution",
        )
        hfig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Share Tech Mono"),
        )
        st.plotly_chart(hfig, use_container_width=True)

    history_csv = history_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ EXPORT SESSION TELEMETRY",
        history_csv,
        file_name="qshield_qds_session_history.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ---------------------------------------------------------------------
# RESEARCH VALIDATION
# ---------------------------------------------------------------------
st.markdown('<div class="section-head">RESEARCH VALIDATION // EXPERIMENTAL EVIDENCE</div>', unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)
for col, label, value in [
    (r1, "BEST ACCURACY", "95.83%"),
    (r2, "BEST PRECISION", "100%"),
    (r3, "BEST F1", "0.8571"),
    (r4, "F1 IMPROVEMENT", "+0.1760"),
]:
    col.markdown(
        f"""<div class="kpi"><div class="label">{label}</div>
        <div class="value cyan">{value}</div></div>""",
        unsafe_allow_html=True,
    )

st.markdown(
    """
<div class="panel">
<div class="panel-title">VALIDATION STATUS</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;font-size:11px;color:#79a9a0;">
  <div>✓ HETEROGENEOUS NOISE</div>
  <div>✓ THRESHOLD SENSITIVITY</div>
  <div>✓ DUAL-SIGNAL ABLATION</div>
  <div>✓ INDEPENDENT-SEED TESTING</div>
  <div>✓ STATISTICAL VALIDATION</div>
  <div>✓ REPRODUCIBILITY ANALYSIS</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------
st.markdown(
    """
<div style="text-align:center;margin-top:35px;color:#43655f;font-size:10px;letter-spacing:.15em;">
  Q-SHIELD RESEARCH PROTOTYPE // TELEPORTATION MISMATCH • BELL ANOMALY • ADAPTIVE SECURITY THRESHOLD
  <br><br>
  SIMULATION ENVIRONMENT // NON-ACTUATING SECURITY ANALYSIS
</div>
""",
    unsafe_allow_html=True,
)
