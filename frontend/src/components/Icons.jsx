/** Minimal inline SVG icons — no external dependency */

const s = { width: 16, height: 16, fill: "none", stroke: "currentColor", strokeWidth: 1.5, strokeLinecap: "round", strokeLinejoin: "round", viewBox: "0 0 24 24" };

export const IconDashboard = () => (
  <svg {...s}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
);

export const IconChart = () => (
  <svg {...s}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
);

export const IconAlert = () => (
  <svg {...s}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
);

export const IconTerminal = () => (
  <svg {...s}><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
);

export const IconHealth = () => (
  <svg {...s}><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
);
