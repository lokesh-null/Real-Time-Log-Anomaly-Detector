import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend,
} from "recharts";

const C = {
  rate: "#E5383B",
  base: "#FCF1D0",
  grid: "rgba(255,255,255,0.04)",
  axis: "#5A6170",
  tipBg: "#0D1C42",
  tipBdr: "rgba(255,255,255,0.1)",
};

function Tip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: C.tipBg, border: `1px solid ${C.tipBdr}`, borderRadius: 4, padding: "8px 12px", fontFamily: "inherit", fontSize: "0.72rem" }}>
      <div style={{ color: "#9DA3AE", marginBottom: 4 }}>{label}</div>
      {payload.map((e) => (
        <div key={e.name} style={{ color: e.color, display: "flex", justifyContent: "space-between", gap: 14 }}>
          <span>{e.name === "error_rate" ? "Error Rate" : "Baseline"}</span>
          <span>{e.value}%</span>
        </div>
      ))}
    </div>
  );
}

export default function ErrorRateChart({ data, compact }) {
  if (!data?.length) {
    return <div className="chart-empty">Waiting for live data…</div>;
  }
  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 6, right: 10, left: compact ? -14 : -6, bottom: 2 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={C.grid} vertical={false} />
          <XAxis dataKey="time" tick={{ fill: C.axis, fontSize: 10 }} tickLine={false} axisLine={{ stroke: C.grid }} interval="preserveStartEnd" minTickGap={50} />
          <YAxis tick={{ fill: C.axis, fontSize: 10 }} tickLine={false} axisLine={{ stroke: C.grid }} tickFormatter={(v) => `${v}%`} domain={[0, "auto"]} width={compact ? 36 : 46} />
          <Tooltip content={<Tip />} />
          {!compact && (
            <Legend verticalAlign="top" height={22} formatter={(v) => v === "error_rate" ? "Error Rate" : "Baseline"} wrapperStyle={{ fontSize: "0.68rem" }} />
          )}
          <Line type="monotone" dataKey="error_rate" stroke={C.rate} strokeWidth={2} dot={false} activeDot={{ r: 3 }} isAnimationActive={false} name="error_rate" />
          <Line type="monotone" dataKey="baseline" stroke={C.base} strokeWidth={1.5} strokeDasharray="6 3" dot={false} activeDot={{ r: 2 }} isAnimationActive={false} name="baseline" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
