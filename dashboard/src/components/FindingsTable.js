import { useState } from "react";

const SEV_COLOR = { CRITICAL: "#ef4444", HIGH: "#f97316", MEDIUM: "#eab308", LOW: "#22c55e", INFO: "#94a3b8" };
const SEV_BG    = { CRITICAL: "#450a0a", HIGH: "#431407", MEDIUM: "#422006", LOW: "#052e16", INFO: "#1e293b" };

export default function FindingsTable({ findings, scan }) {
  const [filter, setFilter] = useState("ALL");
  const [search, setSearch] = useState("");
  const [expanded, setExpanded] = useState(null);

  const filtered = findings.filter(f => {
    if (filter !== "ALL" && f.severity !== filter) return false;
    if (search && !f.title.toLowerCase().includes(search.toLowerCase()) &&
        !(f.file_path || "").toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const card = { background: "#1e293b", borderRadius: 12, border: "1px solid #334155" };
  const btn = (active) => ({
    padding: "5px 12px", borderRadius: 5, border: "none", cursor: "pointer", fontSize: 12,
    background: active ? "#0ea5e9" : "#334155", color: active ? "#fff" : "#94a3b8", fontWeight: 500
  });

  if (!scan) return <div style={{ ...card, padding: 32, color: "#64748b", textAlign: "center" }}>Run a scan first</div>;

  return (
    <div style={card}>
      <div style={{ padding: "16px 20px", borderBottom: "1px solid #334155", display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ color: "#38bdf8", fontWeight: 600, fontSize: 14 }}>Findings</span>
        <span style={{ color: "#64748b", fontSize: 12 }}>({filtered.length} shown)</span>
        <div style={{ marginLeft: "auto", display: "flex", gap: 6, flexWrap: "wrap" }}>
          {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map(s => (
            <button key={s} style={btn(filter === s)} onClick={() => setFilter(s)}>{s}</button>
          ))}
          <input
            placeholder="Search..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ padding: "5px 10px", borderRadius: 5, border: "1px solid #334155", background: "#0f172a", color: "#e2e8f0", fontSize: 12, width: 140 }}
          />
        </div>
      </div>

      <div style={{ maxHeight: 600, overflowY: "auto" }}>
        {filtered.length === 0 ? (
          <div style={{ padding: 40, textAlign: "center", color: "#64748b" }}>No findings match the filter 🎉</div>
        ) : filtered.map((f, i) => (
          <div key={f.fingerprint || i}
            onClick={() => setExpanded(expanded === i ? null : i)}
            style={{ padding: "12px 20px", borderBottom: "1px solid #1e293b", cursor: "pointer",
              background: expanded === i ? "#0f172a" : "transparent",
              transition: "background 0.15s" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ padding: "2px 8px", borderRadius: 4, fontSize: 11, fontWeight: 600,
                background: SEV_BG[f.severity], color: SEV_COLOR[f.severity] }}>{f.severity}</span>
              <span style={{ fontSize: 12, color: "#64748b", background: "#334155", padding: "2px 7px", borderRadius: 4 }}>{f.scanner}</span>
              <span style={{ fontSize: 13, color: "#e2e8f0", fontWeight: 500, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{f.title}</span>
              <span style={{ fontSize: 11, color: "#64748b" }}>{expanded === i ? "▲" : "▼"}</span>
            </div>
            {f.file_path && <div style={{ fontSize: 11, color: "#64748b", marginTop: 4, marginLeft: 2 }}>📄 {f.file_path}{f.line_number ? `:${f.line_number}` : ""}</div>}

            {expanded === i && (
              <div style={{ marginTop: 10, padding: 12, background: "#1e293b", borderRadius: 8 }}>
                <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 6 }}>{f.description}</div>
                {f.cve && <div style={{ fontSize: 11, color: "#f97316" }}>CVE: {f.cve}</div>}
                {f.remediation && <div style={{ fontSize: 11, color: "#22c55e", marginTop: 4 }}>Fix: {f.remediation}</div>}
                {f.url && <div style={{ fontSize: 11, color: "#38bdf8", marginTop: 4 }}>URL: {f.url}</div>}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
