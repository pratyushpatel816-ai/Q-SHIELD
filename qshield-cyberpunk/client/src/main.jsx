import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const QDS_ATTACKS = [
  ["Legitimate communication", "none"],
  ["Digital signature forgery", "forgery"],
  ["Signer impersonation", "impersonation"],
  ["Replay attack", "replay"],
  ["Unauthorized verification", "unauthorized_verification"],
];

const QUANTUM_ATTACKS = [
  ["No quantum attack", "none"],
  ["Pauli-X manipulation", "pauli_x"],
  ["Pauli-Y manipulation", "pauli_y"],
  ["Pauli-Z manipulation", "pauli_z"],
  ["Entanglement disruption", "entanglement_disruption"],
];

const initialLogs = [
  "[SYSTEM] Q-SHIELD control plane initialized",
  "[SYSTEM] QDS verification layer available",
  "[SYSTEM] dual-signal detector armed",
  "[SYSTEM] physical actuation disabled",
];

function App() {
  const [view, setView] = useState("command");
  const [qdsAttack, setQdsAttack] = useState("none");
  const [quantumAttack, setQuantumAttack] = useState("none");
  const [message, setMessage] = useState("INSTALL_FIRMWARE");
  const [verifier, setVerifier] = useState("BOB");
  const [noise, setNoise] = useState("none");
  const [noiseProbability, setNoiseProbability] = useState(0);
  const [basis, setBasis] = useState("Z");
  const [shots, setShots] = useState(1024);
  const [result, setResult] = useState(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [logs, setLogs] = useState(initialLogs);
  const [events, setEvents] = useState([]);
  const [ticks, setTicks] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setTicks((value) => value + 1), 900);
    return () => clearInterval(timer);
  }, []);

  const metrics = useMemo(() => ({
    score: Number(result?.qshield?.security_score ?? 0),
    threshold: Number(result?.qshield?.adaptive_threshold ?? 0.26),
    mismatch: Number(result?.quantum?.mismatch_rate ?? 0),
    bell: Number(result?.qshield?.bell_anomaly_score ?? 0),
    noise: Number(result?.qshield?.estimated_noise ?? noiseProbability),
  }), [result, noiseProbability]);

  const threat = result?.final_decision === "SECURITY THREAT DETECTED";

  function appendLog(lines) {
  const entries = Array.isArray(lines) ? lines : [lines];

  setLogs((current) => [
    ...current,
    ...entries,
  ].slice(-12));
}

  async function runScan() {
    setRunning(true);
    setError("");
    appendLog([
      `[${new Date().toLocaleTimeString()}] scan requested`,
      `[SCAN] qds=${qdsAttack} quantum=${quantumAttack} shots=${shots}`,
    ]);

    try {
      const response = await fetch("/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          qds_attack: qdsAttack,
          quantum_attack: quantumAttack,
          verifier_id: verifier,
          noise_type: noise,
          noise_probability: Number(noiseProbability),
          basis,
          shots: Number(shots),
          bit: 0,
        }),
      });

      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Backend request failed");

      setResult(payload);
      setEvents((current) => [{
        id: `${Date.now()}-${current.length}`,
        time: new Date().toLocaleTimeString(),
        decision: payload.final_decision,
        score: Number(payload.qshield?.security_score ?? 0),
        qds: payload.qds?.verification?.final_decision ?? "UNKNOWN",
      }, ...current].slice(0, 20));
      appendLog([
        `[QDS] ${payload.qds?.verification?.final_decision ?? "UNKNOWN"}`,
        `[Q-SHIELD] score=${Number(payload.qshield?.security_score ?? 0).toFixed(6)}`,
        `[RESULT] ${payload.final_decision}`,
      ]);
    } catch (scanError) {
      setError(scanError.message);
      appendLog(`[ERROR] ${scanError.message}`);
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="app-shell">
      <div className="ambient-grid" />
      <div className="scan-line" />
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark">Q</div>
          <div><strong>Q—SHIELD</strong><span>QUANTUM SECURITY PLATFORM</span></div>
        </div>
        <div className="system-state"><i /> CONTROL PLANE ONLINE <b>SIMULATION</b></div>
      </header>

      <div className="workspace">
        <aside className="sidebar">
          <div className="sidebar-label">WORKSPACES</div>
          {[['command','Command center'],['lab','Quantum lab'],['qds','QDS security'],['forensics','Forensics'],['research','Research']].map(([key, label]) => (
            <button key={key} className={view === key ? "nav-item active" : "nav-item"} onClick={() => setView(key)}>{label}</button>
          ))}
          <div className="sidebar-foot"><span>BUILD</span><strong>STAGE 1</strong><small>UI foundation / non-actuating</small></div>
        </aside>

        <main className="content">
          <section className="page-heading">
            <div><span className="eyebrow">// Q-SHIELD CONTROL SYSTEM</span><h1>{view === "command" ? "Command center" : view === "lab" ? "Quantum channel lab" : view === "qds" ? "QDS security lab" : view === "forensics" ? "Threat forensics" : "Research validation"}</h1><p>Operator interface for controlled quantum-security experiments.</p></div>
            <div className="core-orbit"><div>Q</div><span /><span /><span /></div>
          </section>

          <section className="kpi-row">
            <Kpi label="ENGINE" value="ONLINE" tone="green" /><Kpi label="DETECTION LAYERS" value="02" tone="cyan" /><Kpi label="EVENTS" value={String(events.length).padStart(2, "0")} tone="violet" /><Kpi label="ACTUATION" value="DISABLED" tone="amber" />
          </section>

          {view === "research" ? <Research /> : view === "forensics" ? <Forensics events={events} /> : (
            <>
              <section className="panel scan-panel">
                <div className="panel-heading"><span>01 / EXPERIMENT CONTROL</span><em>AUTHORIZED OPERATOR</em></div>
                <div className="form-grid">
                  <Select label="QDS ATTACK" value={qdsAttack} onChange={setQdsAttack} options={QDS_ATTACKS} />
                  <Select label="QUANTUM CHANNEL" value={quantumAttack} onChange={setQuantumAttack} options={QUANTUM_ATTACKS} />
                  <Field label="MESSAGE" value={message} onChange={setMessage} />
                  <Select label="VERIFIER" value={verifier} onChange={setVerifier} options={[["BOB", "BOB"], ["INTRUDER", "INTRUDER"]]} />
                  <Select label="NOISE MODEL" value={noise} onChange={setNoise} options={[["none", "none"], ["bit_flip", "bit_flip"], ["phase_flip", "phase_flip"], ["depolarizing", "depolarizing"], ["readout", "readout"]]} />
                  <Select label="BASIS" value={basis} onChange={setBasis} options={[["Z", "Z"], ["X", "X"], ["Y", "Y"]]} />
                </div>
                <div className="range-grid"><Range label="NOISE PROBABILITY" value={noiseProbability} min="0" max="0.20" step="0.01" onChange={setNoiseProbability} /><Range label="QUANTUM SHOTS" value={shots} min="256" max="2048" step="256" onChange={setShots} /></div>
                <button className="primary-action" onClick={runScan} disabled={running}>{running ? "SCANNING QUANTUM CHANNEL..." : "INITIATE SECURITY SCAN"}</button>
                {error && <div className="error-box">{error}</div>}
              </section>

              <section className={threat ? "decision-card threat" : "decision-card"}><div className="decision-icon">{threat ? "!" : result ? "✓" : "·"}</div><div><span>SECURITY DECISION</span><h2>{result?.final_decision || "AWAITING SCAN"}</h2><p>{result ? "Decision generated by the connected QDS and Q-SHIELD backend." : "Select a test vector and initiate a controlled scan."}</p></div><strong>0x{Math.floor(metrics.score * 0xffffff).toString(16).padStart(6, "0").toUpperCase()}</strong></section>

              <section className="metric-grid"><Metric label="QDS" value={result?.qds?.verification?.final_decision || "—"} /><Metric label="DETECTOR" value={result?.qshield?.decision || "—"} /><Metric label="SCORE" value={metrics.score.toFixed(4)} /><Metric label="THRESHOLD" value={metrics.threshold.toFixed(4)} /><Metric label="MISMATCH" value={metrics.mismatch.toFixed(4)} /><Metric label="BELL" value={metrics.bell.toFixed(4)} /></section>

              <section className="two-column"><Panel title="QUANTUM TOPOLOGY"><Topology threat={threat} running={running} /></Panel><Panel title="DUAL-SIGNAL TELEMETRY"><Telemetry metrics={metrics} /></Panel></section>
              <section className="two-column"><Panel title="ANALYST TERMINAL"><div className="terminal">{logs.map((line, index) => <div key={index}>{line}</div>)}<span className="cursor">█</span></div></Panel><Panel title="QDS SECURITY CHECKS"><Checks verification={result?.qds?.verification} /></Panel></section>
            </>
          )}
        </main>
      </div>
      <footer>Q—SHIELD / STAGE 1 UI FOUNDATION / SIMULATION MODE / NO PHYSICAL ACTUATION</footer>
    </div>
  );
}

function Kpi({ label, value, tone }) { return <div className="kpi"><span>{label}</span><strong className={tone}>{value}</strong></div>; }
function Metric({ label, value }) { return <div className="metric"><span>{label}</span><strong>{value}</strong></div>; }
function Panel({ title, children }) { return <div className="panel"><div className="panel-heading"><span>{title}</span><em>LIVE VIEW</em></div>{children}</div>; }
function Select({ label, value, onChange, options }) { return <label className="field"><span>{label}</span><select value={value} onChange={(event) => onChange(event.target.value)}>{options.map(([text, option]) => <option key={option} value={option}>{text}</option>)}</select></label>; }
function Field({ label, value, onChange }) { return <label className="field"><span>{label}</span><input value={value} onChange={(event) => onChange(event.target.value)} /></label>; }
function Range({ label, value, min, max, step, onChange }) { return <label className="range-field"><span>{label}<b>{value}</b></span><input type="range" value={value} min={min} max={max} step={step} onChange={(event) => onChange(event.target.value)} /></label>; }
function Topology({ threat, running }) { return <div className={threat ? "topology threat" : "topology"}><div>ALICE<small>QDS SIGNER</small></div><i /> <div>BELL<small>ENTANGLEMENT</small></div><i /><div>Q—SHIELD<small>DETECTOR</small></div><i /><div>BOB<small>VERIFIER</small></div>{running && <b className="topology-pulse" />}</div>; }
function Telemetry({ metrics }) { return <div className="telemetry">{[["MISMATCH", metrics.mismatch], ["BELL ANOMALY", metrics.bell], ["THRESHOLD", metrics.threshold], ["NOISE", metrics.noise]].map(([name, value]) => <div className="telemetry-row" key={name}><span>{name}<b>{value.toFixed(4)}</b></span><div><i style={{ width: `${Math.min(100, value * 100)}%` }} /></div></div>)}</div>; }
function Checks({ verification }) { const rows = [["MESSAGE INTEGRITY", verification?.valid_message], ["AUTHORIZATION", verification?.authorized_verifier], ["SIGNATURE", verification?.signature_valid], ["REPLAY CONTROL", verification ? !verification.replay_detected : null]]; return <div className="checks">{rows.map(([name, ok]) => <div key={name}><span>{name}</span><b className={ok === false ? "bad" : ok === true ? "good" : "wait"}>{ok === null || ok === undefined ? "WAIT" : ok ? "PASS" : "BLOCK"}</b></div>)}{verification?.reason?.length ? <p>{verification.reason.join(" // ")}</p> : null}</div>; }
function Forensics({ events }) { return <section className="panel"><div className="panel-heading"><span>EVENT EVIDENCE</span><em>{events.length} RECORDS</em></div>{events.length ? events.map((event) => <div className="event-row" key={event.id}><span>{event.time}</span><b>{event.qds}</b><span>{event.score.toFixed(5)}</span><strong>{event.decision}</strong></div>) : <p className="empty">No scan events recorded in this session.</p>}</section>; }
function Research() { return <section className="panel research-copy"><div className="panel-heading"><span>RESEARCH VALIDATION</span><em>STATIC REFERENCE</em></div><h2>Validated backend evidence</h2><p>Research metrics must be loaded from versioned experiment artifacts before being presented as current production telemetry. This workspace is intentionally separated from live security decisions.</p><ul><li>Independent-seed validation</li><li>Dual-signal ablation</li><li>Threshold sensitivity</li><li>Reproducibility and limitations</li></ul></section>; }

createRoot(document.getElementById("root")).render(<App />);
