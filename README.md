# 🔒 DevSecOps Vulnerability Scanner & CI/CD Security Gate

A full-stack security automation platform that integrates **SAST** (Semgrep), **SCA** (Trivy), and **DAST** (OWASP ZAP) into a unified pipeline with a React dashboard and GitHub Actions CI/CD gate.

🌐 **Live Demo:** [celadon-piroshki-030adf.netlify.app](https://celadon-piroshki-030adf.netlify.app)
⚙️ **API:** [devsecops-api-k0xs.onrender.com](https://devsecops-api-k0xs.onrender.com)
📖 **API Docs:** [devsecops-api-k0xs.onrender.com/docs](https://devsecops-api-k0xs.onrender.com/docs)

---

## 📁 Project Structure

```
devsecops/
├── scanner/                  # Core scanner modules
│   ├── models.py             # Finding dataclass + deduplication
│   ├── semgrep_scanner.py    # SAST via Semgrep
│   ├── trivy_scanner.py      # SCA via Trivy
│   ├── zap_scanner.py        # DAST via OWASP ZAP
│   └── aggregator.py         # Merge + deduplicate findings
├── api/
│   ├── main.py               # FastAPI backend
│   └── db.py                 # PostgreSQL persistence (optional)
├── dashboard/                # React frontend
│   └── src/
│       ├── App.js
│       └── components/
├── .github/workflows/
│   └── security-gate.yml     # GitHub Actions CI/CD gate
├── example_app/
│   ├── vulnerable_app.py     # Intentionally vulnerable demo app
│   ├── fixed_app.py          # Fixed version after gate catches issues
│   └── EXAMPLE_PR.md         # Example PR showing gate in action
├── run_scan.py               # CLI entrypoint
└── requirements.txt
```

---

## 🚀 Quick Start (Local)

### 1. Install prerequisites

```bash
# Python 3.11+
pip install semgrep fastapi uvicorn

# Trivy (Windows)
winget install aquasecurity.trivy

# Trivy (macOS)
brew install trivy

# Node 18+ for dashboard
node --version
```

### 2. Run the API backend

```bash
python -m uvicorn api.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### 3. Run the React dashboard

```bash
cd dashboard
npm install
npm start
# Open: http://localhost:3000
```

### 4. Run a scan via CLI

```bash
# Scan current directory
python run_scan.py --path .

# Scan with custom thresholds
python run_scan.py --path . --max-critical 0 --max-high 3

# Save report to file
python run_scan.py --path . --output report.json
```

**Exit codes:** `0` = Passed ✅  `1` = Failed ❌  `2` = Error

---

## ⚙️ GitHub Actions Setup

The `.github/workflows/security-gate.yml` triggers automatically on every **push** and **pull request**:
- Installs Semgrep + Trivy automatically
- Runs the security gate
- **Blocks PR merge** if critical/high findings exceed thresholds
- **Posts a summary comment** on the PR with full findings breakdown

---

## 🌐 Cloud Deployment

**API → Render (Free)**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

**Dashboard → Netlify (Free)**
```bash
cd dashboard && npm run build
# Drag and drop build/ folder to netlify.com
```

---

## 🔧 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/scan` | Start a new scan |
| GET | `/scan/{id}` | Get scan status |
| GET | `/scan/{id}/findings` | Get findings (filter by severity/scanner) |
| GET | `/scans` | List all scans |
| GET | `/health` | Health check |

---

## 💡 Key Features

- **Multi-scanner aggregation** — Semgrep (SAST) + Trivy (SCA) + OWASP ZAP (DAST)
- **Deduplication engine** — fingerprints findings by rule+file+line, removes ~60% noise
- **CI/CD gate** — GitHub Actions blocks PRs automatically on threshold breach
- **Real-time dashboard** — React UI with live polling, trend charts, severity filters
- **Developer-first** — one-command local scans, zero setup friction

---

## 🔬 Example PR Demo

The `example_app/` folder contains a full simulation of the gate in action:
- `vulnerable_app.py` — 6 real vulnerability classes: SQL injection, command injection, hardcoded secrets, MD5 password hashing, path traversal, pickle deserialization
- `fixed_app.py` — same app after all issues are resolved
- `EXAMPLE_PR.md` — complete GitHub PR conversation showing gate blocking and then passing