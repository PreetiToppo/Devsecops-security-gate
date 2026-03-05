"""
Optional PostgreSQL persistence — swap in-memory store for this.

Usage:
  1. Set DATABASE_URL env var: postgresql://user:pass@localhost/devsecops
  2. Run: python db.py  (creates tables)
  3. In main.py replace scan_store dict with DB calls below
"""
import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/devsecops")


def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id     TEXT PRIMARY KEY,
                    status      TEXT NOT NULL,
                    started_at  DOUBLE PRECISION,
                    completed_at DOUBLE PRECISION,
                    finding_count INTEGER DEFAULT 0,
                    passed_gate BOOLEAN,
                    summary     JSONB,
                    findings    JSONB DEFAULT '[]'
                );
            """)
        conn.commit()
    print("DB initialized.")


def save_scan(scan: dict):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO scans (scan_id, status, started_at, completed_at,
                    finding_count, passed_gate, summary, findings)
                VALUES (%(scan_id)s, %(status)s, %(started_at)s, %(completed_at)s,
                    %(finding_count)s, %(passed_gate)s, %(summary)s, %(findings)s)
                ON CONFLICT (scan_id) DO UPDATE SET
                    status=EXCLUDED.status,
                    completed_at=EXCLUDED.completed_at,
                    finding_count=EXCLUDED.finding_count,
                    passed_gate=EXCLUDED.passed_gate,
                    summary=EXCLUDED.summary,
                    findings=EXCLUDED.findings
            """, {**scan,
                  "summary": json.dumps(scan.get("summary")),
                  "findings": json.dumps(scan.get("findings", []))})
        conn.commit()


def load_scan(scan_id: str) -> dict | None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scans WHERE scan_id=%s", (scan_id,))
            row = cur.fetchone()
            if not row:
                return None
            row = dict(row)
            row["findings"] = json.loads(row["findings"]) if row["findings"] else []
            row["summary"] = json.loads(row["summary"]) if row["summary"] else {}
            return row


def list_scans() -> list[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT scan_id, status, started_at, completed_at, finding_count, passed_gate, summary FROM scans ORDER BY started_at DESC")
            return [dict(r) for r in cur.fetchall()]


if __name__ == "__main__":
    init_db()
