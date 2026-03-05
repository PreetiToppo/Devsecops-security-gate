import { useState, useEffect } from "react";
import ScanLauncher from "./components/ScanLauncher";
import ScanHistory from "./components/ScanHistory";
import FindingsTable from "./components/FindingsTable";
import SummaryCards from "./components/SummaryCards";
import TrendChart from "./components/TrendChart";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function App() {
  const [scans, setScans] = useState([]);
  const [activeScan, setActiveScan] = useState(null);
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState("dashboard");

  // Poll for scan updates
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API}/scans`);
        const data = await res.json();
        setScans(data.reverse());
        // Auto-select latest
        if (data.length > 0 && !activeScan) setActiveScan(data[0]);
      } catch {}
    }, 3000);
    return () => clearInterval(interval);
  }, [activeScan]);

  // Load findings when activeScan changes
  useEffect(() => {
    if (!activeScan?.scan_id || activeScan.status !== "completed") return;
    fetch(`${API}/scan/${activeScan.scan_id}/findings`)
      .then(r => r.json())
      .then(d => setFindings(d.findings || []));
  }, [activeScan]);

  const startScan = async (config) => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
      });
      const scan = await res.json();
      setActiveScan(scan);
      setFindings([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0f172a", color: "#e2e8f0", fontFamily: "Inter, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#1e293b", borderBottom: "1px solid #334155", padding: "16px 32px", display: "flex", alignItems: "center", gap: 16 }}>
        <span style={{ fontSize: 22, fontWeight: 700, color: "#38bdf8" }}>🔒 DevSecOps Gate</span>
        <span style={{ color: "#64748b", fontSize: 13 }}>Security Automation Platform</span>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          {["dashboard", "findings", "history"].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "6px 16px", borderRadius: 6, border: "none", cursor: "pointer", fontSize: 13, fontWeight: 500,
              background: tab === t ? "#0ea5e9" : "#334155", color: tab === t ? "#fff" : "#94a3b8"
            }}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
          ))}
        </div>
      </div>

      <div style={{ padding: "24px 32px", maxWidth: 1400, margin: "0 auto" }}>
        {tab === "dashboard" && (
          <>
            <div style={{ display: "grid", gridTemplateColumns: "340px 1fr", gap: 24, marginBottom: 24 }}>
              <ScanLauncher onScan={startScan} loading={loading} />
              <SummaryCards scan={activeScan} />
            </div>
            <TrendChart scans={scans} />
          </>
        )}
        {tab === "findings" && <FindingsTable findings={findings} scan={activeScan} />}
        {tab === "history" && <ScanHistory scans={scans} onSelect={s => { setActiveScan(s); setTab("findings"); }} />}
      </div>
    </div>
  );
}
