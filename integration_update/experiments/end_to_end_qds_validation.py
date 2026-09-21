"""End-to-end Q-SHIELD QDS validation harness.

Runs only when the quantum dependency stack is available. It records a
blocking preflight result instead of fabricating end-to-end outcomes.
"""
import csv, json, sys, traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'experiments' / 'results'
OUT.mkdir(parents=True, exist_ok=True)
summary = {'status': 'BLOCKED', 'scope': 'end_to_end_qds', 'checks': [], 'limitations': []}

try:
    from qshield.protocol.payload import CanonicalPayload
    from qshield.protocol.signature import SignatureGenerator
    from qshield.protocol.verifier import SignatureVerifier
    summary['checks'].append({'check': 'quantum_stack_import', 'passed': True})
except Exception as exc:
    summary['checks'].append({'check': 'quantum_stack_import', 'passed': False, 'error': f'{type(exc).__name__}: {exc}'})
    summary['limitations'].append('Qiskit/quantum dependency stack is unavailable; end-to-end execution was not performed.')
    (OUT / 'end_to_end_qds_validation_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
    raise SystemExit(2)

# Deterministic baseline only after dependencies are available.
payload = CanonicalPayload.create(expiry_minutes=10)
generator = SignatureGenerator(shots=256)
signature = generator.generate(payload, signature_length=8)
verifier = SignatureVerifier(shots=256)
result = verifier.verify(payload, signature)
summary.update({'status': 'EXECUTED', 'baseline_result': result})
(OUT / 'end_to_end_qds_validation_summary.json').write_text(json.dumps(summary, indent=2, default=str), encoding='utf-8')
print(json.dumps(summary, indent=2, default=str))
