export default function StatusCard({ label, value, sub, colorClass }) {
  return (
    <div className="metric" role="region" aria-label={label}>
      <div className="metric__label">{label}</div>
      <div className={`metric__value ${colorClass || ""}`}>{value}</div>
      {sub && <div className="metric__sub">{sub}</div>}
    </div>
  );
}
