export default function SummaryCards({ scan }) {
  const card = { background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155" };

  if (!scan) return (
    <div style={{ ...card, display: "flex", alignItems: "center", justifyContent: "center", color: "#64748b" }}>
      No scan selected — run a scan to see results
    </div>
  );

  const s = scan.summary || {};
  const statusColor = scan.status === "completed"
    ? (scan.passed_gate ? "#22c55e" : "#ef4444")
    : scan.status === "running" ? "#f59e0b" : "#64748b";

  const severities = [
    { key: "CRITICAL", color: "#ef4444", bg: "#450a0a" },
    { key: "HIGH",     color: "#f97316", bg: "#431407" },
    { key: "MEDIUM",   color: "#eab308", bg: "#422006" },
    { key: "LOW",      color: "#22c55e", bg: "#052e16" },
    { key: "INFO",     color: "#94a3b8", bg: "#1e293b" },
  ];

  return (
    <div style={card}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
        <div>
          <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>
            Scan {scan.scan_id?.slice(0, 8)}...
          </div>
          <div style={{ fontSize: 12, color: statusColor, fontWeight: 500, marginTop: 2 }}>
            {scan.status === "running" ? "⏳ Running..." : scan.status === "completed" ? (scan.passed_gate ? "✅ Gate PASSED" : "❌ Gate FAILED") : scan.status}
          </div>
        </div>
        <div style={{ marginLeft: "auto", textAlign: "right" }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: "#38bdf8" }}>{scan.finding_count || 0}</div>
          <div style={{ fontSize: 11, color: "#64748b" }}>Total findings</div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 8 }}>
        {severities.map(({ key, color, bg }) => (
          <div key={key} style={{ background: bg, borderRadius: 8, padding: "10px 6px", textAlign: "center" }}>
            <div style={{ fontSize: 20, fontWeight: 700, color }}>{s[key] ?? 0}</div>
            <div style={{ fontSize: 10, color: "#64748b", marginTop: 2 }}>{key}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
