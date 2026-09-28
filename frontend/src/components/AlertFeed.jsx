/**
 * AlertFeed — Displays recent anomaly alerts, newest first.
 * Severity badges use color + text (never color alone).
 * Bounded to ~50 alerts via the data hook.
 */

export default function AlertFeed({ alerts }) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="alert-feed-empty">
        No alerts yet — waiting for anomaly events
      </div>
    );
  }

  return (
    <div className="alert-feed" role="log" aria-label="Alert feed" aria-live="polite">
      {alerts.map((alert) => (
        <AlertItem key={alert.id} alert={alert} />
      ))}
    </div>
  );
}

function AlertItem({ alert }) {
  const severityKey = alert.severity.toLowerCase();
  const badgeClass = `severity-badge severity-badge--${severityKey}`;
  const timeStr = formatAlertTime(alert.timestamp);
  const rateStr =
    alert.error_rate !== undefined
      ? `${(alert.error_rate * 100).toFixed(1)}%`
      : "";

  return (
    <div className="alert-item" role="article" aria-label={`${alert.severity} alert`}>
      <div className="alert-item__severity-col">
        <span className={badgeClass}>
          <span className="severity-badge__dot" aria-hidden="true" />
          {alert.severity}
        </span>
      </div>
      <div className="alert-item__body">
        <div className="alert-item__message">{alert.message}</div>
        <div className="alert-item__meta">
          {rateStr && <span>{rateStr}</span>}
          {alert.deviation !== undefined && (
            <span>{alert.deviation.toFixed(1)}σ</span>
          )}
          <span>{timeStr}</span>
        </div>
      </div>
    </div>
  );
}

function formatAlertTime(isoString) {
  try {
    const d = new Date(isoString);
    if (isNaN(d.getTime())) return "--:--:--";
    return d.toLocaleTimeString("en-US", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return "--:--:--";
  }
}
