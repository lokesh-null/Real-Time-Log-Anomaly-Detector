import { useState, useEffect } from "react";

const NGINX_BASE = "http://localhost:8080";
const BACKEND_BASE = "http://localhost:8000";
const MICROSERVICE_BASE = "http://localhost:5001";

const PRODUCTS = [
  { id: 101, name: "Enterprise Kubernetes Cluster", price: 499.00, tag: "Infrastructure", icon: "☸️", desc: "Multi-region high-availability cluster" },
  { id: 102, name: "AI Log Stream Accelerator", price: 199.00, tag: "Observability", icon: "⚡", desc: "Sub-millisecond log ingestion pipeline" },
  { id: 103, name: "Cloud Sentinel Anomaly Engine", price: 899.00, tag: "AI / ML", icon: "🛡️", desc: "Rolling Z-score anomaly detector" },
  { id: 104, name: "PostgreSQL High-Availability Node", price: 299.00, tag: "Database", icon: "🐘", desc: "Automated failover & read replicas" },
];

export default function StorefrontPage({ stats }) {
  const [cart, setCart] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [checkoutResult, setCheckoutResult] = useState(null);
  const [outageActive, setOutageActive] = useState(false);
  const [recentRequests, setRecentRequests] = useState([]);

  // Fetch initial outage status
  useEffect(() => {
    const checkOutage = async () => {
      try {
        const res = await fetch(`${BACKEND_BASE}/api/simulator/status`);
        if (res.ok) {
          const data = await res.json();
          setOutageActive(data.mode === "payment_outage" || data.mode === "anomaly");
        }
      } catch {}
    };
    checkOutage();
  }, []);

  const addToCart = (product) => {
    setCart((prev) => [...prev, product]);
    logClientAction("INFO", `Added ${product.name} to cart ($${product.price})`);
  };

  const clearCart = () => setCart([]);

  const logClientAction = (level, msg) => {
    const ts = new Date().toLocaleTimeString();
    setRecentRequests((prev) => [{ ts, level, msg, id: Date.now() + Math.random() }, ...prev.slice(0, 7)]);
  };

  const toggleOutage = async () => {
    const nextState = !outageActive;
    setOutageActive(nextState);
    try {
      // Toggle on backend and microservice
      await fetch(`${MICROSERVICE_BASE}/chaos/${nextState ? "inject/payment-outage" : "recover"}`, { method: "POST" }).catch(() => {});
      await fetch(`${BACKEND_BASE}/api/shop/chaos/toggle-outage?enable=${nextState}`, { method: "POST" }).catch(() => {});
      logClientAction(nextState ? "CRITICAL" : "INFO", `Payment Gateway Outage toggled to: ${nextState ? "ACTIVE (504)" : "OFF (200 OK)"}`);
    } catch (e) {
      console.error(e);
    }
  };

  const handleCheckout = async (singleItem = null) => {
    setProcessing(true);
    setCheckoutResult(null);

    const itemsToPay = singleItem ? [singleItem] : cart.length > 0 ? cart : [PRODUCTS[0]];
    const totalAmount = itemsToPay.reduce((sum, item) => sum + item.price, 0);

    const startTime = performance.now();
    try {
      // Send real HTTP request to NGINX (Port 8080) -> Microservice (Port 5001)
      let res;
      try {
        res = await fetch(`${NGINX_BASE}/api/payments/charge`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ order_id: `ord_${Date.now()}`, amount: totalAmount })
        });
      } catch (nginxErr) {
        // Fallback directly to microservice or backend
        res = await fetch(`${MICROSERVICE_BASE}/api/payments/charge`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ order_id: `ord_${Date.now()}`, amount: totalAmount })
        });
      }

      const duration = Math.round(performance.now() - startTime);
      const data = await res.json();

      if (res.ok) {
        setCheckoutResult({
          success: true,
          status: 200,
          duration,
          orderId: data.transaction_id || `ord_${Date.now().toString().slice(-5)}`,
          amount: totalAmount,
          message: "Payment authorized successfully via Stripe Bank Gateway."
        });
        logClientAction("INFO", `HTTP 200 OK - Payment Authorized ($${totalAmount}) [${duration}ms]`);
        if (!singleItem) setCart([]);
      } else {
        setCheckoutResult({
          success: false,
          status: res.status,
          duration,
          message: data.detail || "504 Gateway Timeout: Bank payment network unreachable."
        });
        logClientAction("ERROR", `HTTP ${res.status} - Payment Gateway Timeout ($${totalAmount}) [${duration}ms]`);
      }
    } catch (err) {
      const duration = Math.round(performance.now() - startTime);
      setCheckoutResult({
        success: false,
        status: 504,
        duration,
        message: "HTTP 504: Upstream Payment Gateway unreachable."
      });
      logClientAction("ERROR", `HTTP 504 - Upstream Service Connection Failed [${duration}ms]`);
    } finally {
      setProcessing(false);
    }
  };

  const cartTotal = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className="page store-page">
      {/* Store Header & Chaos Controller */}
      <div className="store-header">
        <div className="store-header__info">
          <h2>🛒 CLOUDMART STOREFRONT</h2>
          <p>Real E-Commerce target application generating live HTTP traffic through NGINX (Port 8080)</p>
        </div>

        <div className="store-chaos-box">
          <div className="store-chaos-status">
            <span className={`store-status-dot ${outageActive ? "store-status-dot--outage" : "store-status-dot--healthy"}`} />
            <span>Gateway: <strong>{outageActive ? "OUTAGE (504 Timeout)" : "HEALTHY (200 OK)"}</strong></span>
          </div>
          <button
            className={`store-chaos-btn ${outageActive ? "store-chaos-btn--recover" : "store-chaos-btn--inject"}`}
            onClick={toggleOutage}
          >
            {outageActive ? "🟢 Restore Gateway (200 OK)" : "🚨 Inject Outage (504 Timeout)"}
          </button>
        </div>
      </div>

      {/* Checkout Alert Banner */}
      {checkoutResult && (
        <div className={`store-result-banner ${checkoutResult.success ? "store-result-banner--ok" : "store-result-banner--fail"}`}>
          <div className="store-result-content">
            <span className="store-result-icon">{checkoutResult.success ? "✅" : "❌"}</span>
            <div>
              <strong>{checkoutResult.success ? `Payment Succeeded — HTTP ${checkoutResult.status} OK` : `Payment Failed — HTTP ${checkoutResult.status} Gateway Timeout`}</strong>
              <p>{checkoutResult.message} (Latency: {checkoutResult.duration}ms)</p>
            </div>
          </div>
          <button className="store-result-close" onClick={() => setCheckoutResult(null)}>✕</button>
        </div>
      )}

      {/* Store Grid */}
      <div className="store-layout">
        {/* Products List */}
        <div className="store-products-col">
          <h3 className="store-section-title">📦 Available Products</h3>
          <div className="store-products-grid">
            {PRODUCTS.map((p) => (
              <div key={p.id} className="store-product-card">
                <div className="store-product-icon">{p.icon}</div>
                <div className="store-product-details">
                  <span className="store-product-tag">{p.tag}</span>
                  <h4>{p.name}</h4>
                  <p>{p.desc}</p>
                  <div className="store-product-price-row">
                    <span className="store-product-price">${p.price.toFixed(2)}</span>
                    <div className="store-product-actions">
                      <button className="store-btn-cart" onClick={() => addToCart(p)}>+ Cart</button>
                      <button className="store-btn-buy" onClick={() => handleCheckout(p)} disabled={processing}>
                        {processing ? "Processing..." : "Buy Now"}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sidebar: Cart & Live HTTP Traffic Stream */}
        <div className="store-sidebar-col">
          {/* Cart Card */}
          <div className="store-card">
            <div className="store-card__head">
              <h4>🛍️ Shopping Cart ({cart.length})</h4>
              {cart.length > 0 && <button className="store-btn-link" onClick={clearCart}>Clear</button>}
            </div>
            <div className="store-card__body">
              {cart.length === 0 ? (
                <p className="store-empty-text">Cart is empty. Click "+ Cart" or "Buy Now" on any product.</p>
              ) : (
                <div className="store-cart-items">
                  {cart.map((item, idx) => (
                    <div key={idx} className="store-cart-item">
                      <span>{item.name}</span>
                      <strong>${item.price.toFixed(2)}</strong>
                    </div>
                  ))}
                  <div className="store-cart-total">
                    <span>Total</span>
                    <strong>${cartTotal.toFixed(2)}</strong>
                  </div>
                  <button className="store-btn-checkout" onClick={() => handleCheckout()} disabled={processing}>
                    {processing ? "Connecting to NGINX..." : `Checkout & Pay ($${cartTotal.toFixed(2)})`}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Live HTTP Traffic Inspector */}
          <div className="store-card store-traffic-card">
            <div className="store-card__head">
              <h4>📡 Real HTTP Traffic Sent</h4>
              <span className="store-card-badge">NGINX :8080</span>
            </div>
            <div className="store-card__body store-traffic-list">
              {recentRequests.length === 0 ? (
                <p className="store-empty-text">No requests sent yet. Click any button to fire real HTTP requests.</p>
              ) : (
                recentRequests.map((req) => (
                  <div key={req.id} className={`store-traffic-item store-traffic-item--${req.level.toLowerCase()}`}>
                    <span className="store-traffic-time">{req.ts}</span>
                    <span className={`store-traffic-level sev-badge sev-badge--${req.level.toLowerCase()}`}>{req.level}</span>
                    <span className="store-traffic-msg">{req.msg}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
