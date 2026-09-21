const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json({ limit: "1mb" }));

const PORT = process.env.PORT || 8787;
const PROJECT_ROOT = path.resolve(__dirname, "..");
const PYTHON = process.env.PYTHON || "python";

app.get("/api/health", (_req, res) => {
  res.json({
    status: "ONLINE",
    engine: "Q-SHIELD PYTHON BACKEND",
    mode: "NON-ACTUATING SIMULATION"
  });
});

app.post("/api/scan", (req, res) => {
  const input = JSON.stringify(req.body || {});
  const child = spawn(PYTHON, ["server/bridge.py"], {
    cwd: PROJECT_ROOT,
    stdio: ["pipe", "pipe", "pipe"],
    windowsHide: true
  });

  let stdout = "";
  let stderr = "";

  child.stdout.on("data", d => { stdout += d.toString(); });
  child.stderr.on("data", d => { stderr += d.toString(); });

  child.on("error", err => {
    res.status(500).json({
      error: `Could not start Python backend: ${err.message}`
    });
  });

  child.on("close", code => {
    if (code !== 0) {
      return res.status(500).json({
        error: stderr || `Python backend exited with code ${code}`
      });
    }

    try {
      const payload = JSON.parse(stdout);
      res.json(payload);
    } catch (err) {
      res.status(500).json({
        error: `Invalid backend response: ${err.message}`,
        raw: stdout,
        stderr
      });
    }
  });

  child.stdin.write(input);
  child.stdin.end();
});

app.listen(PORT, () => {
  console.log(`Q-SHIELD API listening on http://localhost:${PORT}`);
});
