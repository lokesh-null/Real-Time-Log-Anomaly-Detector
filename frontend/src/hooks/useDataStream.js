import { useState, useEffect, useRef, useCallback } from "react";
import { getNextMockEvent, getNextMockLog } from "../mockData";

const WS_URL = "ws://localhost:8000/ws";
const RECONNECT_BASE = 1000;
const RECONNECT_MAX = 16000;
const MAX_CHART = 80;
const MAX_ALERTS = 100;
const MAX_LOGS = 200;
const MOCK_INTERVAL = 1500;
const MOCK_LOG_INTERVAL = 600;

export function useDataStream() {
  const [connState, setConnState] = useState("disconnected");
  const [latest, setLatest] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [recovered, setRecovered] = useState(false);
  const [useMock, setUseMock] = useState(false);
  const [stats, setStats] = useState({ totalEvents: 0, totalAlerts: 0, peakRate: 0, uptimeStart: Date.now() });

  const wsRef = useRef(null);
  const delayRef = useRef(RECONNECT_BASE);
  const reconRef = useRef(null);
  const mockRef = useRef(null);
  const mockLogRef = useRef(null);
  const prevSevRef = useRef(null);
  const aidRef = useRef(0);

  const processEvent = useCallback((ev) => {
    try {
      if (ev.error_rate === undefined || ev.severity === undefined || ev.timestamp === undefined) return;

      setLatest(ev);
      setStats((s) => ({
        ...s,
        totalEvents: s.totalEvents + 1,
        totalAlerts: s.totalAlerts + (ev.is_anomaly ? 1 : 0),
        peakRate: Math.max(s.peakRate, ev.error_rate),
      }));

      const prev = prevSevRef.current;
      if (prev && ["CRITICAL", "HIGH", "WARNING"].includes(prev) && ev.severity === "NORMAL" && !ev.is_anomaly) {
        setRecovered(true);
        setTimeout(() => setRecovered(false), 8000);
      } else if (ev.is_anomaly) {
        setRecovered(false);
      }
      prevSevRef.current = ev.severity;

      const pt = { time: fmtTime(ev.timestamp), error_rate: +(ev.error_rate * 100).toFixed(1), baseline: +(ev.baseline * 100).toFixed(1) };
      setChartData((p) => { const n = [...p, pt]; return n.length > MAX_CHART ? n.slice(-MAX_CHART) : n; });

      if (ev.is_anomaly || (prev && ["CRITICAL", "HIGH", "WARNING"].includes(prev) && ev.severity === "NORMAL")) {
        aidRef.current++;
        const a = { id: aidRef.current, timestamp: ev.timestamp, severity: ev.is_anomaly ? ev.severity : "RECOVERED", message: ev.message, error_rate: ev.error_rate, deviation: ev.deviation };
        setAlerts((p) => { const n = [a, ...p]; return n.length > MAX_ALERTS ? n.slice(0, MAX_ALERTS) : n; });
      }
    } catch (e) {
      console.error("[LogSentinel]", e);
    }
  }, []);

  const processLog = useCallback((log) => {
    setLogs((p) => { const n = [...p, { ...log, id: Date.now() + Math.random() }]; return n.length > MAX_LOGS ? n.slice(-MAX_LOGS) : n; });
  }, []);

  const connectWs = useCallback(() => {
    if (useMock) return;
    if (wsRef.current) { wsRef.current.close(); wsRef.current = null; }
    try {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;
      ws.onopen = () => { setConnState("connected"); delayRef.current = RECONNECT_BASE; };
      ws.onmessage = (e) => {
        try {
          const d = JSON.parse(e.data);
          processEvent(d);
          // Also create a synthetic log entry from the event
          processLog({ timestamp: d.timestamp, level: d.is_anomaly ? d.severity : "INFO", message: d.message });
        } catch (err) { /* malformed */ }
      };
      ws.onclose = () => { setConnState("disconnected"); wsRef.current = null; schedRecon(); };
      ws.onerror = () => {};
    } catch { setConnState("disconnected"); schedRecon(); }
  }, [useMock, processEvent, processLog]);

  const schedRecon = useCallback(() => {
    if (reconRef.current) return;
    const d = delayRef.current;
    reconRef.current = setTimeout(() => { reconRef.current = null; delayRef.current = Math.min(d * 2, RECONNECT_MAX); connectWs(); }, d);
  }, [connectWs]);

  useEffect(() => {
    if (useMock) {
      if (wsRef.current) { wsRef.current.close(); wsRef.current = null; }
      if (reconRef.current) { clearTimeout(reconRef.current); reconRef.current = null; }
      setConnState("mock");
      mockRef.current = setInterval(() => processEvent(getNextMockEvent()), MOCK_INTERVAL);
      mockLogRef.current = setInterval(() => processLog(getNextMockLog()), MOCK_LOG_INTERVAL);
      return () => {
        if (mockRef.current) clearInterval(mockRef.current);
        if (mockLogRef.current) clearInterval(mockLogRef.current);
      };
    } else {
      if (mockRef.current) clearInterval(mockRef.current);
      if (mockLogRef.current) clearInterval(mockLogRef.current);
      connectWs();
    }
    return () => {
      if (wsRef.current) { wsRef.current.close(); wsRef.current = null; }
      if (reconRef.current) { clearTimeout(reconRef.current); reconRef.current = null; }
    };
  }, [useMock, connectWs, processEvent, processLog]);

  const toggleMock = useCallback(() => setUseMock((p) => !p), []);

  return { connState, latest, chartData, alerts, logs, recovered, useMock, toggleMock, stats };
}

function fmtTime(iso) {
  try {
    const d = new Date(iso);
    if (isNaN(d.getTime())) return "--:--:--";
    return d.toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch { return "--:--:--"; }
}
