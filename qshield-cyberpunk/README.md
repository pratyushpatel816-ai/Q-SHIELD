# Q-SHIELD Cyberpunk Quantum Defense Console

This is a React + Vite + Node/Express presentation layer for the existing Q-SHIELD Python backend.

## Architecture

Browser (React/Vite)
        |
        v
Node/Express API :8787
        |
        v
server/bridge.py
        |
        +--> QDSProtocol
        +--> QDSAttackSimulator
        +--> TeleportationEngine
        +--> IntegratedQShieldDetector

The validated Python research modules are not replaced.

## Setup

Copy the `client`, `server`, `package.json`, `vite.config.js`, and `index.html`
into the root of your existing:

C:\Users\USER\qshield

The final layout should be:

qshield/
  client/
  server/
  qshield/
  qds/
  experiments/
  tests/
  package.json
  vite.config.js
  index.html

From the project root:

npm install
npm run dev

Open:

http://localhost:5173

The Node API runs at:

http://localhost:8787

## Important

The Node server expects the `python` command to resolve to the same Python
environment that already runs:

python -m experiments.qds_problem_statement_validation

If your Python command is different, set:

PowerShell:
$env:PYTHON="C:\path\to\python.exe"

then:

npm run server

The interface is a simulation/analysis console. It does not actuate physical systems.
