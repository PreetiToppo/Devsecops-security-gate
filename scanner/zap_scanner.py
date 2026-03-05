import subprocess
import json
import time
import os
from .models import Finding


SEVERITY_MAP = {
    "3": "HIGH",
    "2": "MEDIUM",
    "1": "LOW",
    "0": "INFO",
}


def run_zap_baseline(target_url: str) -> list[Finding]:
    """
    Run OWASP ZAP baseline scan against a live URL using Docker.
    Requires Docker to be running.
    """
    print(f"[ZAP] Scanning {target_url}...")

    report_path = "/tmp/zap_report.json"

    result = subprocess.run([
        "docker", "run", "--rm",
        "-v", "/tmp:/zap/wrk/:rw",
        "ghcr.io/zaproxy/zaproxy:stable",
        "zap-baseline.py",
        "-t", target_url,
        "-J", "zap_report.json",
        "-I"  # don't fail on warnings
    ], capture_output=True, text=True, timeout=300)

    findings = []
    if not os.path.exists(report_path):
        print(f"[ZAP] Report not found. stderr: {result.stderr[:300]}")
        return findings

    try:
        with open(report_path) as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ZAP] Failed to parse report: {e}")
        return findings

    for site in data.get("site", []):
        for alert in site.get("alerts", []):
            severity = SEVERITY_MAP.get(str(alert.get("riskcode", "0")), "INFO")
            for instance in alert.get("instances", [{}]):
                findings.append(Finding(
                    scanner="zap",
                    severity=severity,
                    title=alert.get("alert", "Unknown"),
                    description=alert.get("desc", ""),
                    rule_id=str(alert.get("pluginid", "")),
                    url=instance.get("uri"),
                    remediation=alert.get("solution", ""),
                ))

    print(f"[ZAP] Found {len(findings)} alerts.")
    return findings
