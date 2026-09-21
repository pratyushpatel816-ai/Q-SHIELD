
# Q-SHIELD

### Quantum-Inspired Dual-Signal Framework for Threat Detection and Security Verification in Digital Signature Systems

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Quantum Simulation](https://img.shields.io/badge/Quantum-Simulation-purple.svg)](#quantum-security-layer)
[![Security](https://img.shields.io/badge/Domain-Cybersecurity-red.svg)](#security-features)
[![Research Prototype](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg)](#limitations)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Q-SHIELD is a simulation-based quantum cybersecurity research prototype that combines teleportation-based quantum digital signature mechanisms, Bell-state measurement analysis, and classical security validation to detect malicious communication and signature anomalies.**

---

## Overview

Q-SHIELD transforms a quantum digital signature demonstration into an attack-aware and auditable security-verification framework.

The system combines two complementary signals:

1. **Quantum measurement analysis** — teleportation mismatch, Bell-state measurement anomalies, and fidelity or correlation analysis.
2. **Classical security validation** — payload integrity, identity verification, authorization, replay protection, expiry checks, and signature validation.

These signals are processed through a deterministic decision engine that produces:

- `ACCEPT`
- `WARN`
- `REJECT`

The project is designed for controlled simulation, experimental evaluation, cybersecurity research, and future integration with quantum or enterprise security systems.

---

## Key Features

- Teleportation-based quantum digital signature simulation
- Bell-state entanglement and measurement analysis
- Pauli-X, Pauli-Y, and Pauli-Z attack simulation
- Quantum-channel noise and disturbance experiments
- Projective measurement in different bases
- Conditional Pauli correction operations
- Canonical payload generation
- SHA-256 integrity verification
- Identity and authorization validation
- Replay and expiry protection
- Message-tampering detection
- Impersonation and unauthorized-verifier scenarios
- Configurable security thresholds
- Dual-signal verification engine
- Explainable security decisions
- Audit logging and security-event analysis
- Automated unit and integration tests
- Statistical and reproducibility experiments

---

## System Architecture

```text
                  ┌───────────────────────┐
                  │    Payload Creation   │
                  └───────────┬───────────┘
                              │
                  ┌───────────▼───────────┐
                  │ Canonicalization &    │
                  │ SHA-256 Integrity     │
                  └───────────┬───────────┘
                              │
                  ┌───────────▼───────────┐
                  │ Signature Generation  │
                  └───────────┬───────────┘
                              │
              ┌───────────────▼────────────────┐
              │       Quantum Security Layer   │
              │                                │
              │  State Preparation             │
              │  Bell-State Entanglement       │
              │  Teleportation                  │
              │  Measurement & Corrections      │
              │  Noise / Attack Simulation      │
              └───────────────┬────────────────┘
                              │
                  ┌───────────▼───────────┐
                  │ Mismatch & Fidelity   │
                  │ / Correlation Analysis│
                  └───────────┬───────────┘
                              │
              ┌───────────────▼────────────────┐
              │       Classical Security       │
              │                                │
              │ Identity                       │
              │ Authorization                  │
              │ Replay Protection              │
              │ Expiry Validation              │
              │ Signature & Payload Checks     │
              └───────────────┬────────────────┘
                              │
                  ┌───────────▼───────────┐
                  │ Dual-Signal Decision  │
                  │ Engine                │
                  └───────────┬───────────┘
                              │
              ┌───────────────▼────────────────┐
              │       Final Security Decision   │
              │                                │
              │ ACCEPT / WARN / REJECT         │
              └────────────────────────────────┘
```

---

## Security Features

### Quantum Security Simulation

The quantum layer explores:

- Qubit state preparation
- Bell-pair creation
- Quantum teleportation
- Pauli corrections
- X/Y basis transformations
- Projective measurements
- Measurement mismatch
- Fidelity and correlation analysis
- Simulated quantum-channel attacks

### Classical Security Layer

The classical security engine validates:

- Canonical payload integrity
- SHA-256 hashes
- Sender and receiver identities
- Verifier authorization
- Replay attempts
- Expired payloads
- Signature structure and metadata
- Invalid positions, bits, bases, and signature lengths
- Session and schedule consistency

---

## Attack Scenarios

| Attack | Security Target |
|---|---|
| Pauli-X attack | Bit-flip disturbance |
| Pauli-Y attack | Bit-phase-flip disturbance |
| Pauli-Z attack | Phase-flip disturbance |
| Entanglement disruption | Bell-state correlation |
| Channel noise | Measurement reliability |
| Message tampering | Payload integrity |
| Identity impersonation | Authentication |
| Unauthorized verifier | Access control |
| Replay attack | Message freshness |
| Expired payload | Temporal validity |
| Invalid signature | Signature validation |

Detection behavior depends on the implemented validation rules, thresholds, and simulation conditions.

---

## Research Methodology

The research workflow follows:

```text
Literature Review
       ↓
Threat Model
       ↓
Hypothesis Development
       ↓
Controlled Simulation
       ↓
Attack Injection
       ↓
Metric Collection
       ↓
Baseline Comparison
       ↓
Ablation Study
       ↓
Reproducibility Testing
       ↓
Statistical Evaluation
       ↓
Limitations & Future Work
```

The evaluation may include:

- Fixed and adaptive threshold comparisons
- Noise robustness experiments
- Monte Carlo simulations
- Independent random seeds
- Mismatch-only versus Bell-signal-only analysis
- Dual-signal ablation studies
- Confidence and significance analysis
- Detection-performance evaluation

---

## Mathematical Components

The project investigates quantum and statistical mechanisms including:

### Qubit Representation

\[
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle
\]

where:

\[
|\alpha|^2 + |\beta|^2 = 1
\]

### Pauli Operators

\[
X =
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
\]

\[
Y =
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
\]

\[
Z =
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
\]

### Detection Metrics

Where applicable, the evaluation uses:

- Accuracy
- Precision
- Recall
- F1-score
- True-positive rate
- False-positive rate
- Mismatch rate
- Fidelity or correlation measures
- Verification latency
- Computational complexity

All numerical results should be reproduced from the provided experiments and execution environment.

---

## Project Structure

```text
Q-SHIELD/
│
├── qshield/
│   ├── protocol/
│   ├── security/
│   ├── quantum/
│   └── detection/
│
├── tests/
├── experiments/
├── demos/
├── docs/
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

> The exact structure may vary depending on the current repository implementation.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Q-SHIELD.git
cd Q-SHIELD
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Use the dependency versions specified by the repository whenever available.

---

## Running the Prototype

Run the available demonstration scripts from the project directory:

```bash
python demo_phase1.py
python demo_phase2.py
python demo_phase3a.py
python demo_phase3b.py
python demo_phase3c.py
python demo_phase3d.py
```

The available scripts and commands should be verified against the repository's actual file structure.

---

## Running Tests

Execute the test suite using:

```bash
pytest -v
```

The test suite covers relevant protocol, quantum, and security functionality, including scenarios such as:

- Legitimate communication
- Signature generation and verification
- Message tampering
- Quantum attack simulation
- Identity impersonation
- Unauthorized verification
- Replay attacks
- Expired payloads
- Signature validation

Test results should be interpreted according to the specific execution environment and commit.

---

## Research Contribution

Q-SHIELD investigates a dual-signal architecture that combines:

- Teleportation measurement mismatch
- Bell-state measurement anomaly information
- Classical integrity and access-control validation
- Configurable statistical decision rules

The intended contribution is an experimentally evaluated simulation framework for quantum-inspired threat detection under heterogeneous simulated noise.

The results are limited to the evaluated environment and should not be interpreted as proof of universal cryptographic superiority.

---

## Limitations

Q-SHIELD is currently a **software simulation and security-engineering research prototype**.

It does not, by itself, establish:

- Information-theoretic quantum digital signature security
- Security on physical quantum hardware
- Universal resistance to all quantum attacks
- Formal cryptographic security guarantees
- Production readiness without independent security assessment
- Superiority over standardized cryptographic schemes

Further work is required in formal verification, hardware validation, adversarial testing, cryptographic analysis, and independent security review.

---

## Future Roadmap

- [ ] Improve protocol documentation
- [ ] Expand automated security testing
- [ ] Add reproducible experiment configurations
- [ ] Perform additional noise and attack evaluations
- [ ] Validate statistical assumptions
- [ ] Conduct baseline and ablation studies
- [ ] Add performance benchmarking
- [ ] Improve observability and audit reporting
- [ ] Evaluate integration with standardized cryptographic schemes
- [ ] Explore hardware-backed and physical quantum implementations
- [ ] Perform independent security review
- [ ] Develop deployment and enterprise-hardening documentation

---

## Disclaimer

Q-SHIELD is intended for **research, education, controlled simulation, and prototype development**.

It should not be deployed as a security-critical cryptographic system without comprehensive independent review, formal analysis, and appropriate validation.

---

## Team

**Team:** E-Green Quanta

**Project:** Q-SHIELD

**Domain:** Quantum Computing • Cybersecurity • Digital Signatures • Threat Detection

**Application Context:** Smart India Hackathon and academic research

---

## License

This project is distributed under the MIT License unless otherwise specified.

See the [LICENSE](LICENSE) file for details.
