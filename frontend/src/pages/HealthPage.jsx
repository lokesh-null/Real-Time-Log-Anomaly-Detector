/** System Health Page — uptime, timeline, severity distribution */

import StatusCard from "../components/StatusCard";
import { fmtTime, sevColor } from "../utils";

export default function HealthPage({ latest, alerts, stats, chartData }) {
  const has = latest !== null;
  const uptimeMs = Date.now() - stats.uptimeStart;
  const uptimeMin = Math.floor(uptimeMs / 60000);
  const uptimeSec = Math.floor((uptimeMs % 60000) / 1000);
  const uptimeStr = `${uptimeMin}m ${uptimeSec}s`;

  const critCount = alerts.filter((a) => a.severity === "CRITICAL").length;
  const highCount = alerts.filter((a) => a.severity === "HIGH").length;
  const warnCount = alerts.filter((a) => a.severity === "WARNING").length;
  const recCount = alerts.filter((a) => a.severity === "RECOVERED").length;
  const avgRate = chartData.length > 0
    ? (chartData.reduce((s, p) => s + p.error_rate, 0) / chartData.length).toFixed(1)
    : "—";

  // Severity transitions timeline
  const transitions = [];
  let prevSev = null;
  for (const a of [...alerts].reverse()) {
    if (a.severity !== prevSev) {
      transitions.push(a);
      prevSev = a.severity;
    }
  }

  return (
    <div className="page health-page">
      <div className="health-grid">
        <StatusCard label="System Status" value={has ? latest.severity : "WAITING"} colorClass={has ? sevColor(latest.severity) : "metric__value--muted"} />
        <StatusCard label="Uptime" value={uptimeStr} />
        <StatusCard label="Events Processed" value={stats.totalEvents.toLocaleString()} />
        <StatusCard label="Total Anomalies" value={stats.totalAlerts.toString()} colorClass={stats.totalAlerts > 0 ? "metric__value--amber" : ""} />
        <StatusCard label="Peak Error Rate" value={stats.peakRate > 0 ? `${(stats.peakRate * 100).toFixed(1)}%` : "—"} colorClass={stats.peakRate > 0.3 ? "metric__value--red" : ""} />
        <StatusCard label="Avg Error Rate" value={avgRate !== "—" ? `${avgRate}%` : "—"} />
      </div>

      <div className="health-cards">
        {/* Severity Breakdown */}
        <div className="card">
          <div className="card__head">
            <span className="card__title">Severity Breakdown</span>
            <span className="card__badge">{alerts.length} total alerts</span>
          </div>
          <div className="card__body card__body--pad">
            <div style={{ display: "flex", flexDirection: "column", gap: 12, paddingTop: 8 }}>
              <SevBar label="CRITICAL" count={critCount} total={alerts.length} color="var(--red)" />
              <SevBar label="HIGH" count={highCount} total={alerts.length} color="var(--orange)" />
              <SevBar label="WARNING" count={warnCount} total={alerts.length} color="var(--amber)" />
              <SevBar label="RECOVERED" count={recCount} total={alerts.length} color="var(--green)" />
            </div>
          </div>
        </div>

        {/* Severity Timeline */}
        <div className="card">
          <div className="card__head">
            <span className="card__title">State Transitions</span>
            <span className="card__badge">{transitions.length} changes</span>
          </div>
          <div className="card__body">
            <div className="health-timeline">
              {transitions.length === 0 && (
                <div className="timeline-empty">No state transitions yet</div>
              )}
              {transitions.map((t, i) => (
                <div className="timeline-item" key={i}>
                  <span className="timeline-time">{fmtTime(t.timestamp)}</span>
                  <span className={`sev-dot sev-dot--${t.severity.toLowerCase()}`} style={{ marginTop: 4 }} />
                  <span className={`sev-tag sev-tag--${t.severity.toLowerCase()}`}>{t.severity}</span>
                  <span className="timeline-text">{t.message}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SevBar({ label, count, total, color }) {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.72rem", marginBottom: 4 }}>
        <span style={{ color: "var(--text-2)" }}>{label}</span>
        <span style={{ color: "var(--text-3)" }}>{count} ({pct.toFixed(0)}%)</span>
      </div>
      <div style={{ height: 6, borderRadius: 3, background: "var(--border)" }}>
        <div style={{ width: `${pct}%`, height: "100%", borderRadius: 3, background: color, transition: "width 0.3s ease" }} />
      </div>
    </div>
  );
}
