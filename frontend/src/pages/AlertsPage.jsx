/** Dedicated Alerts Page — full alert history with stats */

import StatusCard from "../components/StatusCard";
import AlertFeed from "../components/AlertFeed";

export default function AlertsPage({ alerts, stats, latest }) {
  const has = latest !== null;
  const critCount = alerts.filter((a) => a.severity === "CRITICAL").length;
  const highCount = alerts.filter((a) => a.severity === "HIGH").length;
  const warnCount = alerts.filter((a) => a.severity === "WARNING").length;
  const recCount = alerts.filter((a) => a.severity === "RECOVERED").length;

  return (
    <div className="page alerts-page">
      <div className="alerts-page-head">
        <StatusCard label="Total Alerts" value={alerts.length.toString()} colorClass={alerts.length > 10 ? "metric__value--amber" : ""} />
        <StatusCard label="Critical" value={critCount.toString()} colorClass={critCount > 0 ? "metric__value--red" : ""} />
        <StatusCard label="High / Warning" value={`${highCount} / ${warnCount}`} colorClass={highCount > 0 ? "metric__value--orange" : ""} />
        <StatusCard label="Recovered" value={recCount.toString()} colorClass="metric__value--green" />
      </div>
      <div className="card" style={{ flex: 1 }}>
        <div className="card__head">
          <span className="card__title">Alert History</span>
          <span className="card__badge">
            {has ? `Current: ${latest.severity}` : "No data"} · {alerts.length} total
          </span>
        </div>
        <div className="card__body">
          <AlertFeed alerts={alerts} />
        </div>
      </div>
    </div>
  );
}
