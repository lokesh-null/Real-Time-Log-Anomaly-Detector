/**
 * App.jsx — Log Sentinel
 * Sidebar shell with page routing. No scrolling — full viewport pages.
 * Does NOT implement anomaly detection — only visualizes backend results.
 */

import { useState, useEffect } from "react";
import { useDataStream } from "./hooks/useDataStream";
import { topbarBadge } from "./utils";
import { IconDashboard, IconChart, IconAlert, IconTerminal, IconHealth, IconCart } from "./components/Icons";
import DemoGuideModal from "./components/DemoGuideModal";
import DashboardPage from "./pages/DashboardPage";
import ChartPage from "./pages/ChartPage";
import AlertsPage from "./pages/AlertsPage";
import ConsolePage from "./pages/ConsolePage";
import HealthPage from "./pages/HealthPage";
import StorefrontPage from "./pages/StorefrontPage";

const PAGES = [
  { id: "dashboard", label: "Overview", icon: IconDashboard },
  { id: "chart", label: "Live Chart", icon: IconChart },
  { id: "alerts", label: "Alerts", icon: IconAlert },
  { id: "console", label: "Log Console", icon: IconTerminal },
  { id: "health", label: "System Health", icon: IconHealth },
];


export default function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [guideOpen, setGuideOpen] = useState(false);
  const { connState, latest, chartData, alerts, logs, recovered, useMock, toggleMock, stats } = useDataStream();

  // Live clock
  const [clock, setClock] = useState(fmtClock());
  useEffect(() => {
    const t = setInterval(() => setClock(fmtClock()), 1000);
    return () => clearInterval(t);
  }, []);

  const has = latest !== null;
  const connLabel = connState === "connected" ? "LIVE" : connState === "mock" ? "MOCK" : "DISCONNECTED";
  const connClass = connState === "connected" ? "live" : connState === "mock" ? "mock" : "off";
  const statusBadge = has ? topbarBadge(latest.severity) : "ok";
  const statusText = has ? latest.severity : "WAITING";

  return (
    <div className="app-shell">
      {/* ── Presenter Guide Modal ── */}
      <DemoGuideModal isOpen={guideOpen} onClose={() => setGuideOpen(false)} />

      {/* ── Sidebar ── */}
      <aside className="sidebar" role="navigation" aria-label="Main navigation">
        <div className="sidebar-brand">
          <h1>LOG SENTINEL</h1>
          <p>Anomaly Monitor</p>
        </div>

        <nav className="sidebar-nav">
          {PAGES.map((p) => (
            <button
              key={p.id}
              className={`sidebar-link ${activePage === p.id ? "active" : ""}`}
              onClick={() => setActivePage(p.id)}
              aria-current={activePage === p.id ? "page" : undefined}
              id={`nav-${p.id}`}
            >
              <p.icon />
              <span>{p.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-conn">
            <span className={`sidebar-dot ${connClass}`} />
            <span>{connLabel}</span>
          </div>
          <button className="sidebar-toggle" onClick={toggleMock} id="toggle-mock-btn">
            {useMock ? "GO LIVE" : "USE MOCK"}
          </button>
        </div>
      </aside>

      {/* ── Main Area ── */}
      <div className="main-content">
        <header className="topbar" role="banner">
          <span className="topbar-title">
            {PAGES.find((p) => p.id === activePage)?.label}
          </span>
          <div className="topbar-right">
            <button 
              className="topbar-guide-btn" 
              onClick={() => setGuideOpen(true)}
              title="Open quick manual on how to demonstrate to judges"
            >
              📖 Demo Manual
            </button>
            <div className={`topbar-badge ${statusBadge}`} id="system-status-badge">
              <span className={`sev-dot sev-dot--${statusText.toLowerCase()}`} />
              {statusText}
            </div>
            <span className="topbar-clock">{clock}</span>
          </div>
        </header>

        {/* ── Pages ── */}
        {activePage === "dashboard" && (
          <DashboardPage latest={latest} chartData={chartData} alerts={alerts} recovered={recovered} useMock={useMock} />
        )}
        {activePage === "store" && (
          <StorefrontPage stats={stats} />
        )}
        {activePage === "chart" && (
          <ChartPage latest={latest} chartData={chartData} stats={stats} />
        )}
        {activePage === "alerts" && (
          <AlertsPage alerts={alerts} stats={stats} latest={latest} />
        )}
        {activePage === "console" && (
          <ConsolePage logs={logs} latest={latest} stats={stats} />
        )}
        {activePage === "health" && (
          <HealthPage latest={latest} alerts={alerts} stats={stats} chartData={chartData} />
        )}

      </div>
    </div>
  );
}

function fmtClock() {
  return new Date().toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

