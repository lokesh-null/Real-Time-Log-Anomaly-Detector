/**
 * App.jsx — Log Sentinel Dashboard
 *
 * Single-page real-time monitoring dashboard.
 * Receives data from one shared source (WebSocket or mock).
 * Does NOT implement anomaly detection — only visualizes backend results.
 */

import { useDataStream } from "./hooks/useDataStream";
import StatusCard from "./components/StatusCard";
import ErrorRateChart from "./components/ErrorRateChart";
import AlertFeed from "./components/AlertFeed";

// ── Severity → CSS class mapping ──
function severityToClass(severity) {
  if (!severity) return "waiting";
  const map = {
    NORMAL: "normal",
    WARNING: "warning",
    HIGH: "high",
    CRITICAL: "critical",
    RECOVERED: "recovered",
  };
  return map[severity] || "waiting";
}

// ── Connection label ──
function connectionLabel(state) {
  switch (state) {
    case "connected":
      return "LIVE";
    case "mock":
      return "MOCK";
    case "disconnected":
    default:
      return "DISCONNECTED";
  }
}

export default function App() {
  const {
    connectionState,
    latestEvent,
    chartData,
    alerts,
    isRecovered,
    useMock,
    toggleMock,
  } = useDataStream();

  // Current values (or waiting state)
  const hasData = latestEvent !== null;
  const errorRateDisplay = hasData
    ? `${(latestEvent.error_rate * 100).toFixed(1)}%`
    : "—";
  const baselineDisplay = hasData
    ? `${(latestEvent.baseline * 100).toFixed(1)}%`
    : "—";
  const deviationDisplay = hasData
    ? `${latestEvent.deviation.toFixed(1)}σ`
    : "—";
  const statusDisplay = hasData ? latestEvent.severity : "WAITING";
  const severityClass = hasData
    ? severityToClass(latestEvent.severity)
    : "waiting";

  const errorRateSub = hasData
    ? `${latestEvent.errors} errors / ${latestEvent.total_logs} total`
    : "Waiting for live data";

  return (
    <div className="app-container">
      {/* ── Header ── */}
      <header className="header" role="banner">
        <div className="header-left">
          <h1 className="header-title" id="app-title">LOG SENTINEL</h1>
          <p className="header-subtitle">Real-time anomaly monitoring</p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            onClick={toggleMock}
            style={{
              background: "transparent",
              border: "1px solid var(--border-light)",
              color: "var(--text-secondary)",
              padding: "4px 14px",
              borderRadius: "16px",
              fontSize: "0.72rem",
              cursor: "pointer",
              letterSpacing: "0.04em",
              fontFamily: "inherit",
              transition: "border-color 0.2s",
            }}
            aria-label={useMock ? "Switch to live WebSocket" : "Switch to mock data"}
            id="toggle-mock-btn"
          >
            {useMock ? "GO LIVE" : "USE MOCK"}
          </button>
          <div
            className={`connection-status ${connectionState}`}
            role="status"
            aria-label={`Connection: ${connectionLabel(connectionState)}`}
            id="connection-status"
          >
            <span className="connection-dot" aria-hidden="true" />
            <span>{connectionLabel(connectionState)}</span>
          </div>
        </div>
      </header>

      {/* ── Mock mode banner ── */}
      {useMock && (
        <div className="mock-banner" role="status" id="mock-banner">
          ⚡ Mock mode — generating simulated anomaly data
        </div>
      )}

      {/* ── Recovery banner ── */}
      {isRecovered && (
        <div className="recovery-banner" role="alert" id="recovery-banner">
          <span className="recovery-banner__icon" aria-hidden="true">🟢</span>
          <div>
            <div className="recovery-banner__text">SYSTEM RECOVERED</div>
            <div className="recovery-banner__sub">
              System returned to normal operating range
            </div>
          </div>
        </div>
      )}

      {/* ── Anomaly banner (CRITICAL) ── */}
      {hasData && latestEvent.severity === "CRITICAL" && latestEvent.is_anomaly && (
        <div className="anomaly-banner" role="alert" id="anomaly-banner">
          <span className="anomaly-banner__icon" aria-hidden="true">🚨</span>
          <div>
            <div className="anomaly-banner__text">CRITICAL ANOMALY DETECTED</div>
            <div className="anomaly-banner__sub">
              Error rate: {(latestEvent.error_rate * 100).toFixed(1)}% — Baseline: {(latestEvent.baseline * 100).toFixed(1)}% — Deviation: {latestEvent.deviation.toFixed(1)}σ
            </div>
          </div>
        </div>
      )}

      {/* ── Metrics ── */}
      <div className="metrics-grid" role="region" aria-label="System metrics">
        <StatusCard
          label="Error Rate"
          value={errorRateDisplay}
          sub={errorRateSub}
          severityClass={
            hasData && latestEvent.error_rate > 0.15
              ? severityClass
              : undefined
          }
        />
        <StatusCard
          label="Baseline"
          value={baselineDisplay}
          sub="Rolling average"
        />
        <StatusCard
          label="Deviation"
          value={deviationDisplay}
          sub="Z-score from baseline"
          severityClass={
            hasData && latestEvent.deviation > 2 ? severityClass : undefined
          }
        />
        <StatusCard
          label="System Status"
          value={statusDisplay}
          sub={hasData ? latestEvent.message : "Awaiting first event"}
          severityClass={severityClass}
        />
      </div>

      {/* ── Chart + Alerts grid ── */}
      <div className="dashboard-grid">
        <div className="section">
          <div className="section__header">
            <h2 className="section__title" id="chart-section-title">Error Rate vs Baseline</h2>
            <span className="section__badge">
              {chartData.length > 0
                ? `${chartData.length} data points`
                : "No data"}
            </span>
          </div>
          <ErrorRateChart data={chartData} />
        </div>

        <div className="section">
          <div className="section__header">
            <h2 className="section__title" id="alerts-section-title">Alert Feed</h2>
            <span className="section__badge">
              {alerts.length > 0
                ? `${alerts.length} alert${alerts.length !== 1 ? "s" : ""}`
                : "No alerts"}
            </span>
          </div>
          <AlertFeed alerts={alerts} />
        </div>
      </div>
    </div>
  );
}
