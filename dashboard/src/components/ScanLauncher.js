import { useState } from "react";

export default function ScanLauncher({ onScan, loading }) {
  const [path, setPath] = useState("./");
  const [url, setUrl] = useState("");
  const [dast, setDast] = useState(false);
  const [maxCrit, setMaxCrit] = useState(0);
  const [maxHigh, setMaxHigh] = useState(5);

  const card = { background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155" };
  const input = {
    width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 6,
    color: "#e2e8f0", padding: "8px 10px", fontSize: 13, boxSizing: "border-box"
  };
  const label = { display: "block", fontSize: 12, color: "#94a3b8", marginBottom: 4, marginTop: 12 };

  return (
    <div style={card}>
      <div style={{ fontSize: 15, fontWeight: 600, color: "#38bdf8", marginBottom: 4 }}>🚀 New Scan</div>
      <div style={{ fontSize: 12, color: "#64748b", marginBottom: 12 }}>Configure and launch a security scan</div>

      <label style={label}>Target Path (SAST + SCA)</label>
      <input style={input} value={path} onChange={e => setPath(e.target.value)} placeholder="./my-project" />

      <label style={label}>Target URL (DAST — optional)</label>
      <input style={input} value={url} onChange={e => setUrl(e.target.value)} placeholder="http://localhost:3000" />

      <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 14 }}>
        <input type="checkbox" id="dast" checked={dast} onChange={e => setDast(e.target.checked)} />
        <label htmlFor="dast" style={{ fontSize: 13, color: "#94a3b8", cursor: "pointer" }}>Enable DAST (ZAP)</label>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginTop: 4 }}>
        <div>
          <label style={label}>Max Critical</label>
          <input style={input} type="number" value={maxCrit} onChange={e => setMaxCrit(+e.target.value)} min={0} />
        </div>
        <div>
          <label style={label}>Max High</label>
          <input style={input} type="number" value={maxHigh} onChange={e => setMaxHigh(+e.target.value)} min={0} />
        </div>
      </div>

      <button
        onClick={() => onScan({ target_path: path || null, target_url: url || null, run_dast: dast, max_critical: maxCrit, max_high: maxHigh })}
        disabled={loading}
        style={{
          width: "100%", marginTop: 18, padding: "10px 0", borderRadius: 8, border: "none",
          background: loading ? "#334155" : "#0ea5e9", color: "#fff", fontWeight: 600,
          fontSize: 14, cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Starting scan..." : "▶ Run Security Gate"}
      </button>
    </div>
  );
}
