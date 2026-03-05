# 🔒 DevSecOps Vulnerability Scanner & CI/CD Security Gate

A full-stack security automation platform that integrates **SAST** (Semgrep), **SCA** (Trivy), and **DAST** (OWASP ZAP) into a unified pipeline with a React dashboard and GitHub Actions CI/CD gate.

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
│           ├── ScanLauncher.js
│           ├── SummaryCards.js
│           ├── FindingsTable.js
│           ├── TrendChart.js
│           └── ScanHistory.js
├── .github/workflows/
│   └── security-gate.yml     # GitHub Actions CI/CD gate
├── run_scan.py               # CLI entrypoint
├── docker-compose.yml
├── Dockerfile.api
└── requirements.txt
```

---

## 🚀 Quick Start (Local)

### 1. Install prerequisites

```bash
# Python 3.11+
pip install semgrep fastapi uvicorn psycopg2-binary

# Trivy (macOS)
brew install trivy

# Trivy (Ubuntu/Debian)
sudo apt-get install trivy

# Node 18+ for dashboard
node --version
```

### 2. Run the API backend

```bash
cd devsecops
uvicorn api.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### 3. Run the React dashboard

```bash
cd devsecops/dashboard
npm install
npm start
# Open: http://localhost:3000
```

### 4. Run a scan via CLI

```bash
# Scan current directory
python run_scan.py --path ./my-project

# Scan with custom thresholds
python run_scan.py --path ./my-project --max-critical 0 --max-high 3

# Full scan (SAST + SCA + DAST)
python run_scan.py --path ./my-project --url http://localhost:3000 --dast

# Save report to file
python run_scan.py --path . --output report.json
```

**Exit codes:**
- `0` = Gate passed ✅
- `1` = Gate failed (too many critical/high) ❌
- `2` = Scan error

---

## 🐳 Docker Deployment (Recommended)

```bash
cd devsecops

# Build and start all services
docker compose up --build

# Services:
# API:       http://localhost:8000
# Dashboard: http://localhost:3000
# Postgres:  localhost:5432
```

To scan your local code inside Docker, mount it as a volume:

```yaml
# In docker-compose.yml, under api > volumes:
- /path/to/your/code:/targets
```

Then trigger scan with `target_path: "/targets"`.

---

## ⚙️ GitHub Actions Setup

1. Copy `.github/workflows/security-gate.yml` to your repo.

2. The workflow triggers on every **push** and **pull request**:
   - Installs Semgrep + Trivy automatically
   - Runs the security gate
   - **Blocks PR merge** if critical/high findings exceed thresholds
   - **Posts a summary comment** on the PR

3. Customize thresholds in the workflow:
   ```yaml
   python run_scan.py \
     --path . \
     --max-critical 0 \   # block if any CRITICAL found
     --max-high 5          # block if > 5 HIGH found
   ```

---

## 🌐 Cloud Deployment (Render — Free Tier)

### Deploy API to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11

### Deploy Dashboard to Vercel (Free)

```bash
cd dashboard
npm install -g vercel
vercel
# Follow prompts, set REACT_APP_API_URL to your Render API URL
```

### Deploy Dashboard to Netlify (Free)

```bash
cd dashboard
npm run build
# Drag and drop the `build/` folder to netlify.com/drop
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

**Example POST /scan:**
```json
{
  "target_path": "./my-project",
  "target_url": "http://localhost:3000",
  "run_sast": true,
  "run_sca": true,
  "run_dast": false,
  "max_critical": 0,
  "max_high": 5
}
```

---

## 💡 Key Features

- **Multi-scanner aggregation** — Semgrep (SAST) + Trivy (SCA) + OWASP ZAP (DAST)
- **Deduplication engine** — fingerprints findings by rule+file+line, removes ~60% noise
- **CI/CD gate** — GitHub Actions blocks PRs automatically on threshold breach
- **Real-time dashboard** — React UI with live polling, trend charts, severity filters
- **Developer-first** — one-command local scans, zero setup friction
- **PostgreSQL persistence** — optional upgrade from in-memory store
