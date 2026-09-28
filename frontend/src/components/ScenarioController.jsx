import { useState, useEffect } from "react";

const BACKEND_URL = "http://localhost:8000";

export default function ScenarioController() {
  const [activeMode, setActiveMode] = useState("stopped");
  const [loading, setLoading] = useState(false);
  const [lastCheckoutResult, setLastCheckoutResult] = useState(null);

  const checkStatus = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/simulator/status`);
      if (res.ok) {
        const data = await res.json();
        setActiveMode(data.running ? data.mode : "stopped");
      }
    } catch (e) {
      // Backend might be offline
    }
  };

  useEffect(() => {
    checkStatus();
    const timer = setInterval(checkStatus, 3000);
    return () => clearInterval(timer);
  }, []);

  const triggerMode = async (mode, speed = 0.8) => {
    setLoading(true);
    try {
      if (mode === "stopped") {
        await fetch(`${BACKEND_URL}/api/simulator/stop`, { method: "POST" });
        setActiveMode("stopped");
      } else {
        await fetch(`${BACKEND_URL}/api/simulator/start?mode=${mode}&speed=${speed}`, { method: "POST" });
        setActiveMode(mode);
      }
    } catch (err) {
      console.error("Failed to control traffic:", err);
    } finally {
      setLoading(false);
    }
  };

  const testLiveCheckout = async () => {
    try {
      // Test real microservice on Port 5001 first, fallback to backend
      let res;
      try {
        res = await fetch("http://127.0.0.1:5001/api/payments/charge", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ order_id: "ord_live_click", amount: 149.99 })
        });
      } catch {
        res = await fetch(`${BACKEND_URL}/api/shop/checkout`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
      }
      const data = await res.json();
      if (res.ok) {
        setLastCheckoutResult(`✅ 200 OK (${data.transaction_id || data.order_id || "Success"})`);
      } else {
        setLastCheckoutResult(`❌ ${res.status} ${data.detail || "Payment 504"}`);
      }
    } catch (err) {
      setLastCheckoutResult("❌ Service Unreachable");
    }
    setTimeout(() => setLastCheckoutResult(null), 4000);
  };

  return (
    <div className="scenario-bar">
      <div className="scenario-bar__label">
        <span className="scenario-pulse" />
        <span>LIVE TRAFFIC CONTROLLER</span>
      </div>

      <div className="scenario-bar__actions">
        <button
          className={`scenario-btn ${activeMode === "normal" ? "active scenario-btn--normal" : ""}`}
          onClick={() => triggerMode("normal", 0.7)}
          disabled={loading}
          title="Simulate normal healthy e-commerce shopping traffic (200 OK)"
        >
          🟢 Normal Traffic
        </button>

        <button
          className={`scenario-btn ${activeMode === "payment_outage" || activeMode === "anomaly" ? "active scenario-btn--danger" : ""}`}
          onClick={() => triggerMode("payment_outage", 0.25)}
          disabled={loading}
          title="Inject Stripe Payment Gateway 504 Timeout Outage"
        >
          🚨 Stripe Outage (504)
        </button>

        <button
          className={`scenario-btn ${activeMode === "db_crash" ? "active scenario-btn--danger" : ""}`}
          onClick={() => triggerMode("db_crash", 0.25)}
          disabled={loading}
          title="Inject PostgreSQL Connection Pool Deadlock"
        >
          💥 DB Deadlock (500)
        </button>

        <button
          className={`scenario-btn ${activeMode === "recovery" ? "active scenario-btn--recovery" : ""}`}
          onClick={() => triggerMode("recovery", 0.6)}
          disabled={loading}
          title="Restore healthy state and flush error sliding window"
        >
          🔄 Recover
        </button>

        {activeMode !== "stopped" && (
          <button
            className="scenario-btn scenario-btn--stop"
            onClick={() => triggerMode("stopped")}
            disabled={loading}
            title="Stop background traffic generation"
          >
            ⏹️ Stop
          </button>
        )}

        <button
          className="scenario-btn scenario-btn--checkout"
          onClick={testLiveCheckout}
          title="Send a real HTTP POST /api/shop/checkout request"
        >
          💳 {lastCheckoutResult || "Send Live Checkout"}
        </button>
      </div>
    </div>
  );
}
