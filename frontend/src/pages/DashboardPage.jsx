/** Dashboard Overview — fits in viewport, no scrolling */

import StatusCard from "../components/StatusCard";
import ErrorRateChart from "../components/ErrorRateChart";
import AlertFeed from "../components/AlertFeed";
import ScenarioController from "../components/ScenarioController";
import { sevColor } from "../utils";

export default function DashboardPage({ latest, chartData, alerts, recovered, useMock }) {
  const has = latest !== null;
  const er = has ? `${(latest.error_rate * 100).toFixed(1)}%` : "—";
  const bl = has ? `${(latest.baseline * 100).toFixed(1)}%` : "—";
  const dv = has ? `${latest.deviation.toFixed(1)}σ` : "—";
  const st = has ? latest.severity : "WAITING";
  const sc = has ? sevColor(latest.severity) : "metric__value--muted";

  return (
    <div className="page">
      {/* Scenario & Chaos Bar */}
      <ScenarioController />

      {/* Banners */}
      {useMock && <div className="banner banner--mock">⚡ Mock mode — simulated data active</div>}
      {recovered && (
        <div className="banner banner--ok">
          🟢 SYSTEM RECOVERED <span className="banner__sub">— returned to normal operating range</span>
        </div>
      )}
      {has && latest.severity === "CRITICAL" && latest.is_anomaly && (
        <div className="banner banner--crit">
          🚨 CRITICAL ANOMALY <span className="banner__sub">— {er} error rate · {dv} deviation</span>
        </div>
      )}

      <div className="dash-grid">

        {/* Metrics row */}
        <div className="dash-metrics">
          <StatusCard label="Error Rate" value={er} sub={has ? `${latest.errors} / ${latest.total_logs}` : "—"} colorClass={has && latest.error_rate > 0.15 ? sc : ""} />
          <StatusCard label="Baseline" value={bl} sub="Rolling avg" />
          <StatusCard label="Deviation" value={dv} sub="Z-score" colorClass={has && latest.deviation > 2 ? sc : ""} />
          <StatusCard label="Status" value={st} sub={has ? latest.message : "Awaiting data"} colorClass={sc} />
          <StatusCard label="Total Logs" value={has ? latest.total_logs.toLocaleString() : "—"} sub="Processed" />
        </div>

        {/* Chart */}
        <div className="dash-chart-area">
          <div className="card">
            <div className="card__head">
              <span className="card__title">Error Rate vs Baseline</span>
              <span className="card__badge">{chartData.length} pts</span>
            </div>
            <div className="card__body">
              <ErrorRateChart data={chartData} compact />
            </div>
          </div>
        </div>

        {/* Alerts sidebar */}
        <div className="dash-alerts-area">
          <div className="card">
            <div className="card__head">
              <span className="card__title">Recent Alerts</span>
              <span className="card__badge">{alerts.length}</span>
            </div>
            <div className="card__body">
              <AlertFeed alerts={alerts.slice(0, 30)} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
