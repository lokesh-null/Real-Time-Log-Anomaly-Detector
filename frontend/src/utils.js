export function fmtTime(iso) {
  try {
    const d = new Date(iso);
    if (isNaN(d.getTime())) return "--:--:--";
    return d.toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch { return "--:--:--"; }
}

export function sevColor(severity) {
  const s = severity?.toUpperCase();
  if (s === "CRITICAL") return "metric__value--red";
  if (s === "HIGH") return "metric__value--orange";
  if (s === "WARNING") return "metric__value--amber";
  if (s === "NORMAL" || s === "RECOVERED") return "metric__value--green";
  return "metric__value--muted";
}

export function topbarBadge(severity) {
  const s = severity?.toUpperCase();
  if (s === "CRITICAL") return "danger";
  if (s === "HIGH") return "danger";
  if (s === "WARNING") return "warn";
  return "ok";
}
