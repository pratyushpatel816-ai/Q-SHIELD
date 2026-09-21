import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from qshield.quantum.teleportation import TeleportationEngine
from qshield.detection.integrated_detector import (
    IntegratedQShieldDetector
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Q-SHIELD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 2rem;
    border-radius: 15px;
    background: linear-gradient(
        135deg,
        #111827,
        #1e3a8a
    );
    border: 1px solid #2563eb;
    margin-bottom: 1rem;
}

.safe-box {
    padding: 25px;
    border-radius: 12px;
    background-color: rgba(34,197,94,0.15);
    border: 2px solid #22c55e;
    text-align: center;
}

.attack-box {
    padding: 25px;
    border-radius: 12px;
    background-color: rgba(239,68,68,0.15);
    border: 2px solid #ef4444;
    text-align: center;
}

.medium-box {
    padding: 25px;
    border-radius: 12px;
    background-color: rgba(245,158,11,0.15);
    border: 2px solid #f59e0b;
    text-align: center;
}

[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #334155;
    padding: 12px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

with st.sidebar:

    st.title("⚙️ Simulation Controls")

    st.divider()

    st.subheader("Quantum Configuration")

    shots = st.selectbox(
        "Quantum Shots",
        [256, 512, 1024, 2048],
        index=2
    )

    bit = st.selectbox(
        "Message Bit",
        [0, 1],
        index=0
    )

    basis = st.selectbox(
        "Measurement Basis",
        ["Z", "X", "Y"],
        index=0
    )

    st.divider()

    st.subheader("Channel Configuration")

    noise_type = st.selectbox(
        "Quantum Noise Model",
        [
            "none",
            "bit_flip",
            "phase_flip",
            "depolarizing",
            "readout"
        ]
    )

    noise_probability = st.slider(
        "Noise Probability",
        min_value=0.0,
        max_value=0.30,
        value=0.05,
        step=0.01
    )

    st.divider()

    st.subheader("Security Scenario")

    attack_type = st.selectbox(
        "Attack Scenario",
        [
            "none",
            "pauli_x",
            "pauli_y",
            "pauli_z",
            "entanglement_disruption"
        ]
    )

    st.divider()

    st.subheader("Q-SHIELD Parameters")

    mismatch_weight = st.slider(
        "Mismatch Signal Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    bell_weight = round(
        1.0 - mismatch_weight,
        1
    )

    st.write(
        f"Bell Signal Weight: **{bell_weight:.1f}**"
    )

    base_threshold = st.slider(
        "Base Threshold",
        min_value=0.10,
        max_value=0.40,
        value=0.26,
        step=0.01
    )

    adaptation_factor = st.slider(
        "Adaptation Factor",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1
    )

    max_threshold = st.slider(
        "Maximum Threshold",
        min_value=base_threshold,
        max_value=0.50,
        value=max(0.32, base_threshold),
        step=0.01
    )

    st.divider()

    run_simulation = st.button(
        "🚀 Run Q-SHIELD Analysis",
        use_container_width=True
    )

    clear_history = st.button(
        "🗑️ Clear Session History",
        use_container_width=True
    )


# ============================================================
# CLEAR HISTORY
# ============================================================

if clear_history:

    st.session_state.history = []

    st.success(
        "Session history cleared."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<h1>🛡️ Q-SHIELD</h1>

<h3>
Quantum Attack Detection Under Heterogeneous Quantum Noise
</h3>

<p>
<b>Dual-Signal Quantum Security Architecture</b>
</p>

<p>
• Teleportation Mismatch Analysis<br>
• Bell Measurement Anomaly Detection<br>
• Security-Constrained Adaptive Thresholding
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SYSTEM STATUS
# ============================================================

status_col1, status_col2, status_col3, status_col4 = (
    st.columns(4)
)

status_col1.metric(
    "Quantum Shots",
    shots
)

status_col2.metric(
    "Noise Model",
    noise_type
)

status_col3.metric(
    "Attack Scenario",
    attack_type
)

status_col4.metric(
    "System Status",
    "READY"
)


st.divider()


# ============================================================
# ARCHITECTURE OVERVIEW
# ============================================================

st.subheader(
    "🔬 Q-SHIELD Detection Pipeline"
)

pipeline_cols = st.columns(5)

pipeline = [

    "📡 Quantum State",

    "⚛️ Teleportation",

    "📊 Dual-Signal Analysis",

    "🧠 Adaptive Threshold",

    "🛡️ Security Decision"
]

for col, step in zip(
    pipeline_cols,
    pipeline
):

    with col:
        st.info(step)


st.divider()


# ============================================================
# RUN SIMULATION
# ============================================================

if run_simulation:

    try:

        with st.spinner(
            "Running quantum teleportation and Q-SHIELD security analysis..."
        ):

            # ------------------------------------------------
            # INITIALIZE QUANTUM TELEPORTATION ENGINE
            # ------------------------------------------------

            engine = TeleportationEngine(
                shots=shots
            )


            # ------------------------------------------------
            # RUN QUANTUM EXPERIMENT
            # ------------------------------------------------

            quantum_result = engine.run(

                bit=bit,

                basis=basis,

                noise_type=noise_type,

                noise_probability=noise_probability,

                attack_type=attack_type
            )


            # ------------------------------------------------
            # INITIALIZE INTEGRATED Q-SHIELD DETECTOR
            # ------------------------------------------------

            detector = IntegratedQShieldDetector(

                mismatch_weight=mismatch_weight,

                bell_weight=bell_weight,

                base_threshold=base_threshold,

                adaptation_factor=adaptation_factor,

                max_threshold=max_threshold
            )


            # ------------------------------------------------
            # PERFORM SECURITY ANALYSIS
            # ------------------------------------------------

            security_result = detector.analyze(

                mismatch_rate=
                quantum_result["mismatch_rate"],

                bell_measurements=
                quantum_result["bell_measurements"]
            )


        # ====================================================
        # SAVE RESULT
        # ====================================================

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        combined_result = {

            "timestamp":
            timestamp,

            "noise_type":
            noise_type,

            "noise_probability":
            noise_probability,

            "attack_type":
            attack_type,

            "basis":
            basis,

            "message_bit":
            bit,

            "mismatch_rate":
            quantum_result["mismatch_rate"],

            "bell_anomaly_score":
            security_result["bell_anomaly_score"],

            "security_score":
            security_result["security_score"],

            "adaptive_threshold":
            security_result["adaptive_threshold"],

            "decision_margin":
            security_result["decision_margin"],

            "decision":
            security_result["decision"],

            "severity":
            security_result["severity"],

            "fidelity_proxy":
            quantum_result["fidelity_proxy"]
        }

        st.session_state.history.append(
            combined_result
        )

        st.session_state.latest_result = {
            "quantum_result":
            quantum_result,

            "security_result":
            security_result,

            "combined_result":
            combined_result
        }


    except Exception as e:

        st.error(
            "❌ Q-SHIELD Simulation Error"
        )

        st.exception(e)


# ============================================================
# DISPLAY LATEST RESULT
# ============================================================

if st.session_state.latest_result is not None:

    quantum_result = (
        st.session_state.latest_result[
            "quantum_result"
        ]
    )

    security_result = (
        st.session_state.latest_result[
            "security_result"
        ]
    )

    combined_result = (
        st.session_state.latest_result[
            "combined_result"
        ]
    )


    # ========================================================
    # SECURITY DECISION
    # ========================================================

    st.divider()

    st.subheader(
        "🛡️ Live Q-SHIELD Security Decision"
    )

    if security_result["attack_detected"]:

        if security_result["severity"] == "HIGH":

            st.markdown(f"""
            <div class="attack-box">

            <h1>🚨 ATTACK DETECTED</h1>

            <h2>
            HIGH SEVERITY
            </h2>

            <p>
            Q-SHIELD detected significant abnormal
            quantum channel behaviour.
            </p>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="medium-box">

            <h1>⚠️ ATTACK DETECTED</h1>

            <h2>
            MEDIUM SEVERITY
            </h2>

            <p>
            Suspicious quantum channel disturbance
            exceeded the adaptive security boundary.
            </p>

            </div>
            """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="safe-box">

        <h1>✅ QUANTUM CHANNEL NORMAL</h1>

        <h3>
        NO SIGNIFICANT ATTACK DETECTED
        </h3>

        <p>
        Observed quantum disturbances are currently
        within the adaptive security boundary.
        </p>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # PRIMARY METRICS
    # ========================================================

    st.write("")

    st.subheader(
        "📊 Real-Time Security Metrics"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Security Score",
        f"{security_result['security_score']:.4f}"
    )

    col2.metric(
        "Adaptive Threshold",
        f"{security_result['adaptive_threshold']:.4f}"
    )

    col3.metric(
        "Mismatch Rate",
        f"{quantum_result['mismatch_rate']:.4f}"
    )

    col4.metric(
        "Bell Anomaly",
        f"{security_result['bell_anomaly_score']:.4f}"
    )


    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Decision Margin",
        f"{security_result['decision_margin']:.4f}"
    )

    col6.metric(
        "Estimated Noise",
        f"{security_result['estimated_noise']:.4f}"
    )

    col7.metric(
        "Fidelity Proxy",
        f"{quantum_result['fidelity_proxy']:.4f}"
    )

    col8.metric(
        "Severity",
        security_result["severity"]
    )


    # ========================================================
    # SECURITY SCORE GAUGE
    # ========================================================

    st.divider()

    st.subheader(
        "🎯 Security Score vs Adaptive Decision Boundary"
    )

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number+delta",

            value=
            security_result["security_score"],

            delta={
                "reference":
                security_result["adaptive_threshold"]
            },

            title={
                "text":
                "Q-SHIELD Combined Security Score"
            },

            gauge={

                "axis": {
                    "range": [0, 1]
                },

                "steps": [

                    {
                        "range": [
                            0,
                            security_result[
                                "adaptive_threshold"
                            ]
                        ],

                        "color":
                        "rgba(34,197,94,0.35)"
                    },

                    {
                        "range": [
                            security_result[
                                "adaptive_threshold"
                            ],
                            1
                        ],

                        "color":
                        "rgba(239,68,68,0.30)"
                    }
                ],

                "threshold": {

                    "line": {
                        "color": "red",
                        "width": 5
                    },

                    "thickness": 0.8,

                    "value":
                    security_result[
                        "adaptive_threshold"
                    ]
                }
            }
        )
    )

    gauge.update_layout(
        height=400
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )


    # ========================================================
    # SECURITY SCORE COMPARISON
    # ========================================================

    comparison_col1, comparison_col2 = (
        st.columns(2)
    )


    with comparison_col1:

        st.subheader(
            "📈 Decision Boundary Comparison"
        )

        score_data = pd.DataFrame({

            "Metric": [

                "Security Score",

                "Adaptive Threshold"
            ],

            "Value": [

                security_result[
                    "security_score"
                ],

                security_result[
                    "adaptive_threshold"
                ]
            ]
        })

        fig_score = px.bar(

            score_data,

            x="Metric",

            y="Value",

            text="Value",

            title=
            "Attack Detection Decision"
        )

        fig_score.update_traces(

            texttemplate="%{text:.4f}",

            textposition="outside"
        )

        fig_score.update_yaxes(
            range=[0, 1]
        )

        st.plotly_chart(
            fig_score,
            use_container_width=True
        )


    # ========================================================
    # DUAL SIGNAL ANALYSIS
    # ========================================================

    with comparison_col2:

        st.subheader(
            "⚛️ Dual-Signal Analysis"
        )

        signal_data = pd.DataFrame({

            "Signal": [

                "Teleportation Mismatch",

                "Bell Anomaly"
            ],

            "Score": [

                quantum_result[
                    "mismatch_rate"
                ],

                security_result[
                    "bell_anomaly_score"
                ]
            ]
        })

        fig_signal = px.bar(

            signal_data,

            x="Signal",

            y="Score",

            text="Score",

            title=
            "Quantum Security Signals"
        )

        fig_signal.update_traces(

            texttemplate="%{text:.4f}",

            textposition="outside"
        )

        fig_signal.update_yaxes(
            range=[0, 1]
        )

        st.plotly_chart(
            fig_signal,
            use_container_width=True
        )


    # ========================================================
    # QUANTUM MEASUREMENT RESULTS
    # ========================================================

    st.divider()

    st.subheader(
        "⚛️ Quantum Measurement Results"
    )

    quantum_col1, quantum_col2 = (
        st.columns(2)
    )


    # --------------------------------------------------------
    # TELEPORTATION STATISTICS
    # --------------------------------------------------------

    with quantum_col1:

        st.write(
            "### Teleportation Statistics"
        )

        teleport_data = pd.DataFrame({

            "Outcome": [

                "Matching Shots",

                "Mismatch Shots"
            ],

            "Count": [

                quantum_result[
                    "matching_shots"
                ],

                quantum_result[
                    "mismatch_shots"
                ]
            ]
        })

        fig_teleport = px.bar(

            teleport_data,

            x="Outcome",

            y="Count",

            text="Count",

            title=
            "Teleportation Measurement Outcomes"
        )

        st.plotly_chart(
            fig_teleport,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BELL MEASUREMENT DISTRIBUTION
    # --------------------------------------------------------

    with quantum_col2:

        st.write(
            "### Bell Measurement Distribution"
        )

        bell_data = pd.DataFrame(

            list(
                quantum_result[
                    "bell_measurements"
                ].items()
            ),

            columns=[

                "Bell Outcome",

                "Count"
            ]
        )

        fig_bell = px.bar(

            bell_data,

            x="Bell Outcome",

            y="Count",

            text="Count",

            title=
            "Bell Measurement Pattern"
        )

        st.plotly_chart(
            fig_bell,
            use_container_width=True
        )


    # ========================================================
    # DECISION EXPLANATION
    # ========================================================

    st.divider()

    st.subheader(
        "🧠 Q-SHIELD Decision Explanation"
    )

    if security_result["attack_detected"]:

        st.warning(
            f"""
### Attack Classification: {security_result['severity']}

The combined dual-signal security score is:

**{security_result['security_score']:.4f}**

The dynamically calculated adaptive threshold is:

**{security_result['adaptive_threshold']:.4f}**

Since the security score exceeds the adaptive
decision boundary, Q-SHIELD classifies the
quantum channel as potentially adversarial.

The decision margin is:

**{security_result['decision_margin']:.4f}**
"""
        )

    else:

        st.success(
            f"""
### Channel Classification: NORMAL

The combined dual-signal security score is:

**{security_result['security_score']:.4f}**

The adaptive security threshold is:

**{security_result['adaptive_threshold']:.4f}**

The observed quantum disturbance remains below
the security boundary and is classified as
consistent with legitimate channel conditions.
"""
        )


    # ========================================================
    # EXPERIMENT CONFIGURATION
    # ========================================================

    st.divider()

    st.subheader(
        "⚙️ Experiment Configuration"
    )

    config_data = {

        "Parameter": [

            "Quantum Shots",

            "Message Bit",

            "Measurement Basis",

            "Expected State",

            "Noise Model",

            "Noise Probability",

            "Attack Scenario",

            "Mismatch Weight",

            "Bell Weight",

            "Base Threshold",

            "Adaptation Factor",

            "Maximum Threshold"
        ],

        "Value": [

            shots,

            bit,

            basis,

            quantum_result[
                "expected_state"
            ],

            noise_type,

            noise_probability,

            attack_type,

            mismatch_weight,

            bell_weight,

            base_threshold,

            adaptation_factor,

            max_threshold
        ]
    }

    st.dataframe(

        pd.DataFrame(config_data),

        use_container_width=True,

        hide_index=True
    )


    # ========================================================
    # DOWNLOAD CURRENT RESULT
    # ========================================================

    st.divider()

    st.subheader(
        "📥 Export Security Analysis"
    )

    result_df = pd.DataFrame(
        [combined_result]
    )

    csv_data = result_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label=
        "⬇️ Download Current Analysis Report",

        data=csv_data,

        file_name=
        "qshield_security_analysis.csv",

        mime="text/csv"
    )


    # ========================================================
    # TECHNICAL DETAILS
    # ========================================================

    with st.expander(
        "🔍 View Detailed Q-SHIELD Analysis"
    ):

        st.json({

            "quantum_result":
            quantum_result,

            "security_result":
            security_result
        })


# ============================================================
# SESSION HISTORY
# ============================================================

if len(st.session_state.history) > 0:

    st.divider()

    st.subheader(
        "📈 Session Security Analysis History"
    )

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(

        history_df,

        use_container_width=True,

        hide_index=True
    )


    # --------------------------------------------------------
    # HISTORY VISUALIZATION
    # --------------------------------------------------------

    if len(history_df) > 1:

        fig_history = px.line(

            history_df,

            y=[

                "security_score",

                "adaptive_threshold"
            ],

            markers=True,

            title=
            "Security Score Evolution Across Simulations"
        )

        fig_history.update_layout(

            xaxis_title=
            "Simulation Run",

            yaxis_title=
            "Security Value"
        )

        st.plotly_chart(

            fig_history,

            use_container_width=True
        )


    # --------------------------------------------------------
    # DOWNLOAD SESSION HISTORY
    # --------------------------------------------------------

    history_csv = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label=
        "📥 Download Complete Session History",

        data=history_csv,

        file_name=
        "qshield_session_history.csv",

        mime="text/csv"
    )


# ============================================================
# RESEARCH VALIDATION SECTION
# ============================================================

st.divider()

st.subheader(
    "🔬 Research Validation Highlights"
)

research_col1, research_col2, research_col3, research_col4 = (
    st.columns(4)
)

research_col1.metric(
    "Best Accuracy",
    "95.83%"
)

research_col2.metric(
    "Best F1 Score",
    "0.8571"
)

research_col3.metric(
    "False Positive Rate",
    "0.0000"
)

research_col4.metric(
    "F1 Improvement",
    "+0.1760"
)


st.info(
    """
Q-SHIELD has been experimentally evaluated using heterogeneous
quantum noise models, multiple adversarial attacks, threshold
sensitivity analysis, dual-signal ablation studies, reproducibility
experiments, computational complexity analysis, and statistical
significance testing.

The interactive dashboard above uses the actual Q-SHIELD quantum
simulation and integrated detection pipeline.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("""
### 🛡️ Q-SHIELD Research Prototype

**Dual-Signal Quantum Attack Detection Framework**

Teleportation Mismatch Analysis • Bell Measurement Anomaly Detection • Adaptive Security Thresholding

Research prototype validated through heterogeneous quantum noise experiments,
ablation studies, reproducibility analysis, and statistical validation.
""")