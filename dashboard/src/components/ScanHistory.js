export default function ScanHistory({ scans, onSelect }) {
  const card = { background: "#1e293b", borderRadius: 12, border: "1px solid #334155" };

  return (
    <div style={card}>
      <div style={{ padding: "16px 20px", borderBottom: "1px solid #334155" }}>
        <span style={{ color: "#38bdf8", fontWeight: 600, fontSize: 14 }}>📋 Scan History</span>
      </div>
      {scans.length === 0
        ? <div style={{ padding: 40, color: "#64748b", textAlign: "center" }}>No scans yet</div>
        : scans.map(s => {
            const passed = s.passed_gate;
            const statusColor = s.status === "completed" ? (passed ? "#22c55e" : "#ef4444") : s.status === "running" ? "#f59e0b" : "#64748b";
            return (
              <div key={s.scan_id}
                onClick={() => onSelect(s)}
                style={{ padding: "14px 20px", borderBottom: "1px solid #0f172a", cursor: "pointer",
                  display: "flex", alignItems: "center", gap: 12 }}
                onMouseEnter={e => e.currentTarget.style.background = "#0f172a"}
                onMouseLeave={e => e.currentTarget.style.background = "transparent"}
              >
                <div style={{ width: 8, height: 8, borderRadius: "50%", background: statusColor, flexShrink: 0 }} />
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 13, color: "#e2e8f0", fontWeight: 500 }}>Scan {s.scan_id?.slice(0, 8)}...</div>
                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>
                    {new Date(s.started_at * 1000).toLocaleString()}
                  </div>
                </div>
                {s.summary && (
                  <div style={{ display: "flex", gap: 8, fontSize: 12 }}>
                    <span style={{ color: "#ef4444" }}>C:{s.summary.CRITICAL || 0}</span>
                    <span style={{ color: "#f97316" }}>H:{s.summary.HIGH || 0}</span>
                    <span style={{ color: "#eab308" }}>M:{s.summary.MEDIUM || 0}</span>
                  </div>
                )}
                <div style={{ fontSize: 11, color: statusColor, fontWeight: 600 }}>
                  {s.status === "completed" ? (passed ? "✅ PASS" : "❌ FAIL") : s.status}
                </div>
              </div>
            );
          })
      }
    </div>
  );
}
