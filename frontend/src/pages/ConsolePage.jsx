/** Log Console Page — terminal-style live log viewer */

import { useRef, useEffect } from "react";
import StatusCard from "../components/StatusCard";
import { fmtTime } from "../utils";

export default function ConsolePage({ logs, latest, stats }) {
  const scrollRef = useRef(null);
  const has = latest !== null;

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const infoCount = logs.filter((l) => l.level === "INFO").length;
  const warnCount = logs.filter((l) => l.level === "WARNING").length;
  const errCount = logs.filter((l) => ["ERROR", "CRITICAL"].includes(l.level)).length;

  return (
    <div className="page console-page">
      <div className="console-stats-row">
        <StatusCard label="Total Entries" value={logs.length.toString()} />
        <StatusCard label="Info" value={infoCount.toString()} colorClass="metric__value--green" />
        <StatusCard label="Warnings" value={warnCount.toString()} colorClass={warnCount > 0 ? "metric__value--amber" : ""} />
        <StatusCard label="Errors" value={errCount.toString()} colorClass={errCount > 0 ? "metric__value--red" : ""} />
        <StatusCard label="Events Processed" value={stats.totalEvents.toString()} />
      </div>
      <div className="console-card">
        <div className="console-head">
          <span className="console-head__title">Live Log Stream</span>
          <span className="console-head__count">{logs.length} entries · max 200</span>
        </div>
        <div className="console-body" ref={scrollRef}>
          {logs.length === 0 && (
            <div style={{ padding: 24, color: "var(--text-3)", textAlign: "center", fontFamily: "inherit", fontSize: "0.82rem" }}>
              Waiting for log entries…
            </div>
          )}
          {logs.map((log) => {
            const lvl = log.level?.toLowerCase() || "info";
            return (
              <div className="console-line" key={log.id}>
                <span className="console-ts">{fmtTime(log.timestamp)}</span>
                <span className={`console-lvl console-lvl--${lvl}`}>{log.level}</span>
                <span className="console-msg">{log.message}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
