from dataclasses import dataclass, field
from typing import Optional
import hashlib


@dataclass
class Finding:
    scanner: str          # semgrep | trivy | zap
    severity: str         # CRITICAL | HIGH | MEDIUM | LOW | INFO
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    rule_id: Optional[str] = None
    cve: Optional[str] = None
    remediation: Optional[str] = None
    url: Optional[str] = None         # for ZAP web findings

    @property
    def fingerprint(self) -> str:
        """Unique hash for deduplication across scanners."""
        key = f"{self.rule_id or self.title}:{self.file_path}:{self.line_number}"
        return hashlib.md5(key.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "scanner": self.scanner,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "rule_id": self.rule_id,
            "cve": self.cve,
            "remediation": self.remediation,
            "url": self.url,
            "fingerprint": self.fingerprint,
        }
