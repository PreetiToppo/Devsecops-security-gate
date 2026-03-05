import subprocess
import json
from .models import Finding


SEVERITY_MAP = {
    "CRITICAL": "CRITICAL",
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "LOW": "LOW",
    "UNKNOWN": "INFO",
}


def run_trivy(target_path: str) -> list[Finding]:
    """Run Trivy filesystem scan on target_path and return normalized findings."""
    print(f"[Trivy] Scanning {target_path}...")

    result = subprocess.run(
        ["trivy", "fs", "--format", "json", "--quiet", target_path],
        capture_output=True, text=True
    )

    findings = []
    if not result.stdout.strip():
        print("[Trivy] No output.")
        return findings

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[Trivy] Failed to parse output: {result.stdout[:200]}")
        return findings

    for result_item in data.get("Results", []):
        for vuln in result_item.get("Vulnerabilities", []):
            severity = SEVERITY_MAP.get(vuln.get("Severity", "UNKNOWN"), "INFO")
            findings.append(Finding(
                scanner="trivy",
                severity=severity,
                title=f"{vuln.get('PkgName', '')} - {vuln.get('VulnerabilityID', '')}",
                description=vuln.get("Description", ""),
                file_path=result_item.get("Target"),
                rule_id=vuln.get("VulnerabilityID"),
                cve=vuln.get("VulnerabilityID") if vuln.get("VulnerabilityID", "").startswith("CVE") else None,
                remediation=f"Fix version: {vuln.get('FixedVersion', 'No fix available')}",
            ))

    print(f"[Trivy] Found {len(findings)} vulnerabilities.")
    return findings
