#!/usr/bin/env python3
"""
CLI entry point for the security gate.

Usage:
  python run_scan.py --path ./my-project
  python run_scan.py --path ./my-project --url http://localhost:3000 --dast
  python run_scan.py --path ./my-project --max-critical 0 --max-high 3

Exit codes:
  0 = gate passed (safe to merge)
  1 = gate failed (critical/high threshold exceeded)
  2 = scan error
"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from scanner.aggregator import aggregate_findings, severity_summary, should_fail_gate


def main():
    parser = argparse.ArgumentParser(description="DevSecOps Security Gate")
    parser.add_argument("--path", help="Target directory for SAST + SCA")
    parser.add_argument("--url", help="Target URL for DAST (ZAP)")
    parser.add_argument("--dast", action="store_true", help="Enable DAST scan")
    parser.add_argument("--no-sast", action="store_true", help="Skip SAST (Semgrep)")
    parser.add_argument("--no-sca", action="store_true", help="Skip SCA (Trivy)")
    parser.add_argument("--max-critical", type=int, default=0)
    parser.add_argument("--max-high", type=int, default=5)
    parser.add_argument("--output", help="Write JSON report to file")
    args = parser.parse_args()

    if not args.path and not args.url:
        print("Error: provide --path and/or --url")
        sys.exit(2)

    try:
        findings = aggregate_findings(
            target_path=args.path,
            target_url=args.url,
            run_sast=not args.no_sast,
            run_sca=not args.no_sca,
            run_dast=args.dast,
        )
    except Exception as e:
        print(f"Scan failed: {e}")
        sys.exit(2)

    summary = severity_summary(findings)
    passed = not should_fail_gate(findings, args.max_critical, args.max_high)

    # Print report
    print("\n" + "="*60)
    print("  SECURITY GATE REPORT")
    print("="*60)
    for sev, count in summary.items():
        icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡" if sev == "MEDIUM" else "🟢"
        print(f"  {icon}  {sev:<10} {count}")
    print("-"*60)
    print(f"  Total findings: {len(findings)}")
    print(f"  Gate status:    {'✅ PASSED' if passed else '❌ FAILED'}")
    print("="*60 + "\n")

    # Show critical/high details
    critical_high = [f for f in findings if f.severity in ("CRITICAL", "HIGH")]
    if critical_high:
        print("Critical/High findings:")
        for f in critical_high[:10]:
            loc = f"{f.file_path}:{f.line_number}" if f.file_path else (f.url or "")
            print(f"  [{f.scanner.upper()}] {f.severity} — {f.title}")
            if loc:
                print(f"           at {loc}")

    # Write JSON report
    if args.output:
        report = {
            "summary": summary,
            "passed_gate": passed,
            "findings": [f.to_dict() for f in findings]
        }
        with open(args.output, "w") as fp:
            json.dump(report, fp, indent=2)
        print(f"\nFull report written to {args.output}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
