import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

export function TrendChart({ scans }) {
  const data = scans
    .filter(s => s.status === "completed" && s.summary)
    .slice(0, 10)
    .reverse()
    .map((s, i) => ({
      name: `#${i + 1}`,
      CRITICAL: s.summary.CRITICAL || 0,
      HIGH: s.summary.HIGH || 0,
      MEDIUM: s.summary.MEDIUM || 0,
      LOW: s.summary.LOW || 0,
    }));

  const card = { background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155", marginTop: 24 };

  return (
    <div style={card}>
      <div style={{ fontSize: 14, fontWeight: 600, color: "#38bdf8", marginBottom: 16 }}>📈 Findings Trend (last 10 scans)</div>
      {data.length === 0
        ? <div style={{ color: "#64748b", textAlign: "center", padding: 20 }}>No completed scans yet</div>
        : <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", color: "#e2e8f0" }} />
              <Legend />
              <Bar dataKey="CRITICAL" fill="#ef4444" radius={[3,3,0,0]} />
              <Bar dataKey="HIGH"     fill="#f97316" radius={[3,3,0,0]} />
              <Bar dataKey="MEDIUM"   fill="#eab308" radius={[3,3,0,0]} />
              <Bar dataKey="LOW"      fill="#22c55e" radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
      }
    </div>
  );
}

export default TrendChart;
