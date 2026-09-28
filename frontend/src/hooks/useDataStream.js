import { useState, useEffect, useRef, useCallback } from "react";
import { getNextMockEvent } from "../mockData";

const WS_URL = "ws://localhost:8000/ws";
const RECONNECT_BASE_DELAY = 1000;
const RECONNECT_MAX_DELAY = 16000;
const MAX_CHART_POINTS = 80;
const MAX_ALERTS = 50;
const MOCK_INTERVAL_MS = 1500;

/**
 * Custom hook for the entire data layer.
 * Connects to the backend WebSocket or falls back to mock data.
 *
 * Returns: { connectionState, latestEvent, chartData, alerts, isRecovered, useMock, toggleMock }
 */
export function useDataStream() {
  // "connected" | "disconnected" | "mock"
  const [connectionState, setConnectionState] = useState("disconnected");
  const [latestEvent, setLatestEvent] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [isRecovered, setIsRecovered] = useState(false);
  const [useMock, setUseMock] = useState(false);

  const wsRef = useRef(null);
  const reconnectDelayRef = useRef(RECONNECT_BASE_DELAY);
  const reconnectTimerRef = useRef(null);
  const mockTimerRef = useRef(null);
  const prevSeverityRef = useRef(null);
  const alertIdRef = useRef(0);

  // ── Process an incoming event (from WS or mock) ──
  const processEvent = useCallback((event) => {
    try {
      // Validate minimal required fields
      if (
        event.error_rate === undefined ||
        event.severity === undefined ||
        event.timestamp === undefined
      ) {
        console.warn("[LogSentinel] Malformed event, skipping:", event);
        return;
      }

      setLatestEvent(event);

      // Detect recovery: was anomaly, now normal
      const prev = prevSeverityRef.current;
      if (
        prev &&
        ["CRITICAL", "HIGH", "WARNING"].includes(prev) &&
        event.severity === "NORMAL" &&
        !event.is_anomaly
      ) {
        setIsRecovered(true);
        // Clear recovery banner after 8 seconds
        setTimeout(() => setIsRecovered(false), 8000);
      } else if (event.is_anomaly) {
        setIsRecovered(false);
      }
      prevSeverityRef.current = event.severity;

      // Chart data — keep bounded
      const chartPoint = {
        time: formatTime(event.timestamp),
        error_rate: +(event.error_rate * 100).toFixed(1),
        baseline: +(event.baseline * 100).toFixed(1),
      };
      setChartData((prev) => {
        const next = [...prev, chartPoint];
        return next.length > MAX_CHART_POINTS
          ? next.slice(next.length - MAX_CHART_POINTS)
          : next;
      });

      // Alerts — only anomalies + recovery
      if (event.is_anomaly || (prev && ["CRITICAL", "HIGH", "WARNING"].includes(prev) && event.severity === "NORMAL")) {
        alertIdRef.current += 1;
        const alert = {
          id: alertIdRef.current,
          timestamp: event.timestamp,
          severity: event.is_anomaly ? event.severity : "RECOVERED",
          message: event.message,
          error_rate: event.error_rate,
          deviation: event.deviation,
        };
        setAlerts((prev) => {
          const next = [alert, ...prev];
          return next.length > MAX_ALERTS ? next.slice(0, MAX_ALERTS) : next;
        });
      }
    } catch (err) {
      console.error("[LogSentinel] Error processing event:", err);
    }
  }, []);

  // ── WebSocket connection ──
  const connectWs = useCallback(() => {
    if (useMock) return;

    // Clean up existing
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    try {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnectionState("connected");
        reconnectDelayRef.current = RECONNECT_BASE_DELAY;
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          processEvent(data);
        } catch (err) {
          console.warn("[LogSentinel] Invalid JSON from WebSocket:", err);
        }
      };

      ws.onclose = () => {
        setConnectionState("disconnected");
        wsRef.current = null;
        scheduleReconnect();
      };

      ws.onerror = () => {
        // onclose will fire after this
      };
    } catch (err) {
      setConnectionState("disconnected");
      scheduleReconnect();
    }
  }, [useMock, processEvent]);

  const scheduleReconnect = useCallback(() => {
    if (reconnectTimerRef.current) return;
    const delay = reconnectDelayRef.current;
    reconnectTimerRef.current = setTimeout(() => {
      reconnectTimerRef.current = null;
      reconnectDelayRef.current = Math.min(
        delay * 2,
        RECONNECT_MAX_DELAY
      );
      connectWs();
    }, delay);
  }, [connectWs]);

  // ── Mock data mode ──
  useEffect(() => {
    if (useMock) {
      // Disconnect WS if active
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
        reconnectTimerRef.current = null;
      }

      setConnectionState("mock");

      mockTimerRef.current = setInterval(() => {
        const event = getNextMockEvent();
        processEvent(event);
      }, MOCK_INTERVAL_MS);

      return () => {
        if (mockTimerRef.current) {
          clearInterval(mockTimerRef.current);
          mockTimerRef.current = null;
        }
      };
    } else {
      // Stop mock and try WS
      if (mockTimerRef.current) {
        clearInterval(mockTimerRef.current);
        mockTimerRef.current = null;
      }
      connectWs();
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
        reconnectTimerRef.current = null;
      }
    };
  }, [useMock, connectWs, processEvent]);

  const toggleMock = useCallback(() => {
    setUseMock((prev) => !prev);
  }, []);

  return {
    connectionState,
    latestEvent,
    chartData,
    alerts,
    isRecovered,
    useMock,
    toggleMock,
  };
}

// ── Helpers ──

function formatTime(isoString) {
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
