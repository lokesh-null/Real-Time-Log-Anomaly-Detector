/**
 * StatusCard — Displays a single metric (error rate, baseline, deviation, or status).
 * Follows the shared data contract field names exactly.
 */

export default function StatusCard({ label, value, sub, severityClass }) {
  const valueClass = severityClass
    ? `status-card__value status-card__value--${severityClass}`
    : "status-card__value";

  return (
    <div className="status-card" role="region" aria-label={label}>
      <div className="status-card__label">{label}</div>
      <div className={valueClass}>{value}</div>
      {sub && <div className="status-card__sub">{sub}</div>}
    </div>
  );
}
