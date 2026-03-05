from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scanner.aggregator import aggregate_findings, severity_summary, should_fail_gate

app = FastAPI(title="DevSecOps Security Gate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store (swap for PostgreSQL in production — see db.py)
scan_store: dict = {}


# ── Request/Response Models ──────────────────────────────────────────────────

class ScanRequest(BaseModel):
    target_path: Optional[str] = None
    target_url: Optional[str] = None
    run_sast: bool = True
    run_sca: bool = True
    run_dast: bool = False
    max_critical: int = 0
    max_high: int = 5

class ScanStatus(BaseModel):
    scan_id: str
    status: str       # pending | running | completed | failed
    started_at: float
    completed_at: Optional[float] = None
    finding_count: int = 0
    passed_gate: Optional[bool] = None
    summary: Optional[dict] = None


# ── Background scan job ──────────────────────────────────────────────────────

def run_scan_job(scan_id: str, req: ScanRequest):
    scan_store[scan_id]["status"] = "running"
    try:
        findings = aggregate_findings(
            target_path=req.target_path,
            target_url=req.target_url,
            run_sast=req.run_sast,
            run_sca=req.run_sca,
            run_dast=req.run_dast,
        )
        summary = severity_summary(findings)
        passed = not should_fail_gate(findings, req.max_critical, req.max_high)

        scan_store[scan_id].update({
            "status": "completed",
            "completed_at": time.time(),
            "findings": [f.to_dict() for f in findings],
            "finding_count": len(findings),
            "summary": summary,
            "passed_gate": passed,
        })
    except Exception as e:
        scan_store[scan_id].update({
            "status": "failed",
            "completed_at": time.time(),
            "error": str(e),
        })


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "DevSecOps Security Gate API is running 🔒"}


@app.post("/scan", response_model=ScanStatus)
def start_scan(req: ScanRequest, background_tasks: BackgroundTasks):
    if not req.target_path and not req.target_url:
        raise HTTPException(400, "Provide target_path and/or target_url")

    scan_id = str(uuid.uuid4())
    scan_store[scan_id] = {
        "scan_id": scan_id,
        "status": "pending",
        "started_at": time.time(),
        "finding_count": 0,
        "passed_gate": None,
        "summary": None,
        "findings": [],
    }
    background_tasks.add_task(run_scan_job, scan_id, req)
    return scan_store[scan_id]


@app.get("/scan/{scan_id}", response_model=ScanStatus)
def get_scan_status(scan_id: str):
    if scan_id not in scan_store:
        raise HTTPException(404, "Scan not found")
    s = scan_store[scan_id]
    return {k: v for k, v in s.items() if k != "findings"}


@app.get("/scan/{scan_id}/findings")
def get_findings(scan_id: str, severity: Optional[str] = None, scanner: Optional[str] = None):
    if scan_id not in scan_store:
        raise HTTPException(404, "Scan not found")
    findings = scan_store[scan_id].get("findings", [])
    if severity:
        findings = [f for f in findings if f["severity"] == severity.upper()]
    if scanner:
        findings = [f for f in findings if f["scanner"] == scanner.lower()]
    return {"scan_id": scan_id, "count": len(findings), "findings": findings}


@app.get("/scans")
def list_scans():
    return [
        {k: v for k, v in s.items() if k != "findings"}
        for s in scan_store.values()
    ]


@app.get("/health")
def health():
    return {"status": "ok", "scans_in_memory": len(scan_store)}
