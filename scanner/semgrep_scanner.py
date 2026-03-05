import subprocess
import json
import os
from .models import Finding


SEVERITY_MAP = {
    "ERROR": "HIGH",
    "WARNING": "MEDIUM",
    "INFO": "LOW",
}


def run_semgrep(target_path: str) -> list[Finding]:
    """Run Semgrep SAST scan on target_path and return normalized findings."""
    print(f"[Semgrep] Scanning {target_path}...")

    result = subprocess.run(
    ["python", "-m", "semgrep", "--config=auto", "--json", "--quiet", target_path],
    capture_output=True, text=True
)

    findings = []
    if not result.stdout.strip():
        print("[Semgrep] No output.")
        return findings

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[Semgrep] Failed to parse output: {result.stdout[:200]}")
        return findings

    for r in data.get("results", []):
        severity = SEVERITY_MAP.get(r.get("extra", {}).get("severity", "INFO"), "LOW")
        findings.append(Finding(
            scanner="semgrep",
            severity=severity,
            title=r.get("check_id", "Unknown Rule"),
            description=r.get("extra", {}).get("message", ""),
            file_path=r.get("path"),
            line_number=r.get("start", {}).get("line"),
            rule_id=r.get("check_id"),
            remediation=r.get("extra", {}).get("fix", None),
        ))

    print(f"[Semgrep] Found {len(findings)} issues.")
    return findings
