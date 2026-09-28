import { fmtTime } from "../utils";

export default function AlertFeed({ alerts }) {
  if (!alerts?.length) {
    return <div className="alert-empty">No alerts — system nominal</div>;
  }
  return (
    <div className="alerts-scroll" role="log" aria-label="Alert feed" aria-live="polite">
      {alerts.map((a) => {
        const sev = a.severity.toLowerCase();
        return (
          <div className="alert-row" key={a.id} role="article">
            <span className={`sev-dot sev-dot--${sev}`} />
            <span className={`sev-tag sev-tag--${sev}`}>{a.severity}</span>
            <span className="alert-msg">{a.message}</span>
            <span className="alert-meta">
              {a.error_rate !== undefined ? `${(a.error_rate * 100).toFixed(1)}%` : ""}
              {a.deviation !== undefined ? ` · ${a.deviation.toFixed(1)}σ` : ""}
            </span>
            <span className="alert-meta">{fmtTime(a.timestamp)}</span>
          </div>
        );
      })}
    </div>
  );
}
