/**
 * ErrorRateChart — Real-time line chart showing error_rate and baseline over time.
 * Uses Recharts. Bounded to the latest ~80 data points.
 */

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
} from "recharts";

const CHART_COLORS = {
  errorRate: "#E5383B",
  baseline: "#FCF1D0",
  grid: "rgba(255,255,255,0.04)",
  axis: "#5A6170",
  tooltipBg: "#0D1C42",
  tooltipBorder: "rgba(255,255,255,0.1)",
};

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) return null;

  return (
    <div
      style={{
        background: CHART_COLORS.tooltipBg,
        border: `1px solid ${CHART_COLORS.tooltipBorder}`,
        borderRadius: "6px",
        padding: "10px 14px",
        fontFamily: '"ZCOOL QingKe HuangYou", sans-serif',
        fontSize: "0.78rem",
      }}
    >
      <div style={{ color: "#9DA3AE", marginBottom: "6px" }}>{label}</div>
      {payload.map((entry) => (
        <div
          key={entry.name}
          style={{
            color: entry.color,
            display: "flex",
            justifyContent: "space-between",
            gap: "16px",
          }}
        >
          <span>{entry.name === "error_rate" ? "Error Rate" : "Baseline"}</span>
          <span>{entry.value}%</span>
        </div>
      ))}
    </div>
  );
}

export default function ErrorRateChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-container">
        <div className="chart-empty">Waiting for live data…</div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 8, right: 12, left: -8, bottom: 4 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke={CHART_COLORS.grid}
            vertical={false}
          />
          <XAxis
            dataKey="time"
            tick={{ fill: CHART_COLORS.axis, fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: CHART_COLORS.grid }}
            interval="preserveStartEnd"
            minTickGap={40}
          />
          <YAxis
            tick={{ fill: CHART_COLORS.axis, fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: CHART_COLORS.grid }}
            tickFormatter={(v) => `${v}%`}
            domain={[0, "auto"]}
            width={52}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="top"
            height={28}
            formatter={(value) =>
              value === "error_rate" ? "Error Rate" : "Baseline"
            }
            wrapperStyle={{ fontSize: "0.75rem" }}
          />
          <Line
            type="monotone"
            dataKey="error_rate"
            stroke={CHART_COLORS.errorRate}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: CHART_COLORS.errorRate }}
            isAnimationActive={false}
            name="error_rate"
          />
          <Line
            type="monotone"
            dataKey="baseline"
            stroke={CHART_COLORS.baseline}
            strokeWidth={1.5}
            strokeDasharray="6 3"
            dot={false}
            activeDot={{ r: 3, fill: CHART_COLORS.baseline }}
            isAnimationActive={false}
            name="baseline"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
