/** Dedicated Chart Page — full-width chart with stats strip */

import StatusCard from "../components/StatusCard";
import ErrorRateChart from "../components/ErrorRateChart";
import { sevColor } from "../utils";

export default function ChartPage({ latest, chartData, stats }) {
  const has = latest !== null;
  const er = has ? `${(latest.error_rate * 100).toFixed(1)}%` : "—";
  const bl = has ? `${(latest.baseline * 100).toFixed(1)}%` : "—";
  const pk = stats.peakRate > 0 ? `${(stats.peakRate * 100).toFixed(1)}%` : "—";

  return (
    <div className="page chart-page">
      <div className="chart-page-stats">
        <StatusCard label="Current Error Rate" value={er} colorClass={has && latest.error_rate > 0.15 ? sevColor(latest.severity) : ""} />
        <StatusCard label="Current Baseline" value={bl} />
        <StatusCard label="Peak Error Rate" value={pk} colorClass={stats.peakRate > 0.3 ? "metric__value--red" : ""} />
        <StatusCard label="Data Points" value={chartData.length.toString()} sub={`of ${80} max`} />
      </div>
      <div className="card" style={{ flex: 1 }}>
        <div className="card__head">
          <span className="card__title">Error Rate vs Baseline — Live</span>
          <span className="card__badge">
            {has ? `${latest.severity} · ${(latest.deviation).toFixed(1)}σ` : "No data"}
          </span>
        </div>
        <div className="card__body">
          <ErrorRateChart data={chartData} />
        </div>
      </div>
    </div>
  );
}
