from .models import Finding
from .semgrep_scanner import run_semgrep
from .trivy_scanner import run_trivy
from .zap_scanner import run_zap_baseline
from typing import Optional


def aggregate_findings(
    target_path: Optional[str] = None,
    target_url: Optional[str] = None,
    run_sast: bool = True,
    run_sca: bool = True,
    run_dast: bool = False,
) -> list[Finding]:
    """
    Run all enabled scanners and return deduplicated findings.
    - target_path: local directory for SAST (Semgrep) + SCA (Trivy)
    - target_url:  live URL for DAST (ZAP)
    """
    all_findings: list[Finding] = []

    if run_sast and target_path:
        all_findings.extend(run_semgrep(target_path))

    if run_sca and target_path:
        all_findings.extend(run_trivy(target_path))

    if run_dast and target_url:
        all_findings.extend(run_zap_baseline(target_url))

    # Deduplicate by fingerprint
    seen = set()
    unique = []
    for f in all_findings:
        if f.fingerprint not in seen:
            seen.add(f.fingerprint)
            unique.append(f)

    removed = len(all_findings) - len(unique)
    print(f"[Aggregator] Total: {len(all_findings)}, After dedup: {len(unique)} (-{removed} duplicates)")
    return unique


def severity_summary(findings: list[Finding]) -> dict:
    summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for f in findings:
        summary[f.severity] = summary.get(f.severity, 0) + 1
    return summary


def should_fail_gate(findings: list[Finding], max_critical: int = 0, max_high: int = 0) -> bool:
    """Return True if findings exceed thresholds (blocks CI/CD pipeline)."""
    summary = severity_summary(findings)
    return summary["CRITICAL"] > max_critical or summary["HIGH"] > max_high
