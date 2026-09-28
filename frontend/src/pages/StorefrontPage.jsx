import { useState, useEffect } from "react";

const NGINX_BASE = "http://localhost:8080";
const BACKEND_BASE = "http://localhost:8000";
const MICROSERVICE_BASE = "http://localhost:5001";

const PRODUCTS = [
  { id: 101, name: "Enterprise Kubernetes Pod", category: "Infrastructure", price: 499.00, icon: "☸️", desc: "Multi-region cluster with auto-scaling & load balancer", popular: true },
  { id: 102, name: "Log Stream Accelerator", category: "Observability", price: 199.00, icon: "⚡", desc: "Sub-millisecond high-throughput ingestion engine", popular: false },
  { id: 103, name: "Sentinel AI Shield", category: "Security / ML", price: 899.00, icon: "🛡️", desc: "Rolling Z-score anomaly detector with auto AWS alerting", popular: true },
  { id: 104, name: "PostgreSQL HA Cluster", category: "Databases", price: 299.00, icon: "🐘", desc: "Automated failover with synchronous read replicas", popular: false },
  { id: 105, name: "Redis In-Memory Cache", category: "Databases", price: 149.00, icon: "⚡", desc: "Ultra-low latency session token & rate limit store", popular: false },
  { id: 106, name: "Cloudflare Edge Gateway", category: "Networking", price: 349.00, icon: "🌐", desc: "Global CDN reverse proxy with DDoS mitigation", popular: false },
];

export default function StorefrontPage() {
  const [cart, setCart] = useState([PRODUCTS[0]]);
  const [processing, setProcessing] = useState(false);
  const [activeOutage, setActiveOutage] = useState(null); // null | 'payment' | 'db'
  const [lastOrderResponse, setLastOrderResponse] = useState(null);
  const [recentTraffic, setRecentTraffic] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");

  const categories = ["All", "Infrastructure", "Observability", "Security / ML", "Databases", "Networking"];

  const logTraffic = (status, code, latency, path) => {
    const ts = new Date().toLocaleTimeString();
    setRecentTraffic((prev) => [
      { id: Date.now() + Math.random(), ts, status, code, latency, path },
      ...prev.slice(0, 8)
    ]);
  };

  const setChaosMode = async (mode) => {
    try {
      if (mode === "payment") {
        await fetch(`${MICROSERVICE_BASE}/chaos/inject/payment-outage`, { method: "POST" }).catch(() => {});
        await fetch(`${BACKEND_BASE}/api/shop/chaos/toggle-outage?enable=true`, { method: "POST" }).catch(() => {});
        setActiveOutage("payment");
        logTraffic("CRITICAL", 504, 2, "POST /chaos/inject/payment-outage");
      } else if (mode === "db") {
        await fetch(`${MICROSERVICE_BASE}/chaos/inject/db-deadlock`, { method: "POST" }).catch(() => {});
        setActiveOutage("db");
        logTraffic("CRITICAL", 500, 2, "POST /chaos/inject/db-deadlock");
      } else {
        await fetch(`${MICROSERVICE_BASE}/chaos/recover`, { method: "POST" }).catch(() => {});
        await fetch(`${BACKEND_BASE}/api/shop/chaos/toggle-outage?enable=false`, { method: "POST" }).catch(() => {});
        setActiveOutage(null);
        logTraffic("INFO", 200, 1, "POST /chaos/recover (HEALTHY)");
      }
    } catch (e) {
      console.error(e);
    }
  };

  const addToCart = (product) => {
    setCart((prev) => [...prev, product]);
    logTraffic("INFO", 200, 1, `Cart +1: ${product.name}`);
  };

  const removeFromCart = (index) => {
    setCart((prev) => prev.filter((_, i) => i !== index));
  };

  const clearCart = () => setCart([]);

  const handleCheckout = async (singleProduct = null) => {
    setProcessing(true);
    setLastOrderResponse(null);

    const items = singleProduct ? [singleProduct] : cart.length > 0 ? cart : [PRODUCTS[0]];
    const totalAmount = items.reduce((sum, item) => sum + item.price, 0);
    const orderId = `ORD-${Date.now().toString().slice(-6)}`;

    const startTime = performance.now();
    try {
      let res;
      try {
        res = await fetch(`${NGINX_BASE}/api/payments/charge`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ order_id: orderId, amount: totalAmount })
        });
      } catch (err) {
        res = await fetch(`${MICROSERVICE_BASE}/api/payments/charge`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ order_id: orderId, amount: totalAmount })
        });
      }

      const latency = Math.round(performance.now() - startTime);
      const data = await res.json();

      if (res.ok) {
        setLastOrderResponse({
          success: true,
          status: 200,
          latency,
          orderId,
          amount: totalAmount,
          message: "Payment authorized successfully by Stripe Bank Gateway."
        });
        logTraffic("INFO", 200, latency, `POST /api/payments/charge ($${totalAmount})`);
        if (!singleProduct) setCart([]);
      } else {
        setLastOrderResponse({
          success: false,
          status: res.status,
          latency,
          orderId,
          amount: totalAmount,
          message: data.detail || "504 Gateway Timeout: Stripe payment network unreachable."
        });
        logTraffic("ERROR", res.status, latency, `POST /api/payments/charge ($${totalAmount})`);
      }
    } catch (e) {
      const latency = Math.round(performance.now() - startTime);
      setLastOrderResponse({
        success: false,
        status: 504,
        latency,
        orderId,
        amount: totalAmount,
        message: "HTTP 504 Gateway Timeout: Upstream service unavailable."
      });
      logTraffic("ERROR", 504, latency, `POST /api/payments/charge (FAILED)`);
    } finally {
      setProcessing(false);
    }
  };

  const cartTotal = cart.reduce((sum, item) => sum + item.price, 0);
  const filteredProducts = selectedCategory === "All" 
    ? PRODUCTS 
    : PRODUCTS.filter((p) => p.category === selectedCategory);

  return (
    <div className="page store-container">
      {/* ── Top Hero & Chaos Bar ── */}
      <div className="store-hero">
        <div className="store-hero__left">
          <div className="store-brand-pill">
            <span className="store-pulse" />
            <span>CLOUDMART TARGET APP</span>
            <span className="store-port-tag">NGINX :8080</span>
          </div>
          <h2>Live E-Commerce Microservice</h2>
          <p>Every interaction triggers real TCP HTTP network traffic through NGINX into Log Sentinel</p>
        </div>

        {/* Chaos Controller Panel */}
        <div className="store-chaos-panel">
          <div className="store-chaos-status-bar">
            <span className="chaos-label">GATEWAY HEALTH:</span>
            {activeOutage === "payment" && <span className="chaos-tag chaos-tag--crit">🚨 STRIPE 504 OUTAGE</span>}
            {activeOutage === "db" && <span className="chaos-tag chaos-tag--crit">💥 DB 500 DEADLOCK</span>}
            {!activeOutage && <span className="chaos-tag chaos-tag--ok">🟢 100% HEALTHY (200 OK)</span>}
          </div>
          <div className="store-chaos-btn-group">
            <button
              className={`chaos-pill-btn ${activeOutage === "payment" ? "active chaos-pill-btn--danger" : ""}`}
              onClick={() => setChaosMode(activeOutage === "payment" ? "recover" : "payment")}
              title="Trigger Stripe Payment Gateway 504 Timeout Outage"
            >
              🚨 Inject Stripe Outage (504)
            </button>
            <button
              className={`chaos-pill-btn ${activeOutage === "db" ? "active chaos-pill-btn--danger" : ""}`}
              onClick={() => setChaosMode(activeOutage === "db" ? "recover" : "db")}
              title="Trigger PostgreSQL Connection Deadlock"
            >
              💥 Inject DB Deadlock (500)
            </button>
            <button
              className="chaos-pill-btn chaos-pill-btn--recover"
              onClick={() => setChaosMode("recover")}
              title="Restore all services to normal"
            >
              🔄 Restore All
            </button>
          </div>
        </div>
      </div>

      {/* ── Order Feedback Toast Banner ── */}
      {lastOrderResponse && (
        <div className={`store-toast ${lastOrderResponse.success ? "store-toast--success" : "store-toast--danger"}`}>
          <div className="store-toast__left">
            <span className="store-toast__icon">{lastOrderResponse.success ? "✅" : "🚨"}</span>
            <div>
              <h4>{lastOrderResponse.success ? `Payment Confirmed — HTTP 200 OK` : `Payment Rejected — HTTP ${lastOrderResponse.status} Gateway Timeout`}</h4>
              <p>{lastOrderResponse.message} • Latency: <strong>{lastOrderResponse.latency}ms</strong> • Order: {lastOrderResponse.orderId}</p>
              {!lastOrderResponse.success && (
                <div className="store-toast__alert-badge">
                  <span>⚡ Sentinel Anomaly Triggered → AWS SNS Push Dispatched</span>
                </div>
              )}
            </div>
          </div>
          <button className="store-toast__close" onClick={() => setLastOrderResponse(null)}>✕</button>
        </div>
      )}

      {/* ── Main Layout: Store + Cart & Telemetry ── */}
      <div className="store-grid">
        {/* Left Column: Category Tabs & Products */}
        <div className="store-catalog">
          {/* Category Filter Pills */}
          <div className="store-categories">
            {categories.map((cat) => (
              <button
                key={cat}
                className={`store-cat-pill ${selectedCategory === cat ? "active" : ""}`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Product Cards Grid */}
          <div className="store-products">
            {filteredProducts.map((p) => (
              <div key={p.id} className="store-card">
                <div className="store-card__top">
                  <span className="store-card__icon">{p.icon}</span>
                  {p.popular && <span className="store-badge-popular">POPULAR</span>}
                </div>
                <div className="store-card__meta">
                  <span className="store-card__category">{p.category}</span>
                  <h3>{p.name}</h3>
                  <p>{p.desc}</p>
                </div>
                <div className="store-card__bottom">
                  <div className="store-card__price">
                    <span className="price-curr">$</span>
                    <span className="price-val">{p.price.toFixed(2)}</span>
                  </div>
                  <div className="store-card__actions">
                    <button className="btn-add-cart" onClick={() => addToCart(p)}>+ Cart</button>
                    <button className="btn-instant-buy" onClick={() => handleCheckout(p)} disabled={processing}>
                      {processing ? "..." : "Instant Buy"}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Shopping Cart & Live HTTP Traffic */}
        <div className="store-side-panel">
          {/* Shopping Cart Drawer */}
          <div className="store-panel-card">
            <div className="store-panel-card__head">
              <h3>🛍️ Shopping Cart <span className="cart-count-badge">{cart.length}</span></h3>
              {cart.length > 0 && <button className="btn-text-clear" onClick={clearCart}>Clear</button>}
            </div>
            <div className="store-panel-card__body">
              {cart.length === 0 ? (
                <div className="cart-empty-state">
                  <span>🛒</span>
                  <p>Your cart is empty</p>
                  <small>Click "+ Cart" or "Instant Buy" on any product</small>
                </div>
              ) : (
                <div className="cart-items-list">
                  {cart.map((item, idx) => (
                    <div key={idx} className="cart-item-row">
                      <div className="cart-item-info">
                        <span className="cart-item-icon">{item.icon}</span>
                        <div>
                          <strong>{item.name}</strong>
                          <span className="cart-item-price">${item.price.toFixed(2)}</span>
                        </div>
                      </div>
                      <button className="btn-remove-item" onClick={() => removeFromCart(idx)}>✕</button>
                    </div>
                  ))}

                  <div className="cart-summary-box">
                    <div className="summary-row">
                      <span>Subtotal</span>
                      <span>${cartTotal.toFixed(2)}</span>
                    </div>
                    <div className="summary-row">
                      <span>Tax (0%)</span>
                      <span>$0.00</span>
                    </div>
                    <div className="summary-row total-row">
                      <strong>Total Due</strong>
                      <strong>${cartTotal.toFixed(2)}</strong>
                    </div>
                  </div>

                  <button
                    className="btn-pay-now"
                    onClick={() => handleCheckout()}
                    disabled={processing}
                  >
                    {processing ? "Sending TCP request to NGINX..." : `Place Order & Pay ($${cartTotal.toFixed(2)})`}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Real-time HTTP Traffic Monitor */}
          <div className="store-panel-card">
            <div className="store-panel-card__head">
              <h3>📡 Live NGINX Traffic <span className="port-pill">Port 8080</span></h3>
            </div>
            <div className="store-traffic-box">
              {recentTraffic.length === 0 ? (
                <p className="traffic-empty">Click buttons above to send real HTTP requests</p>
              ) : (
                recentTraffic.map((t) => (
                  <div key={t.id} className={`traffic-log-row traffic-log-row--${t.status.toLowerCase()}`}>
                    <span className="traffic-time">{t.ts}</span>
                    <span className={`traffic-badge traffic-badge--${t.code >= 500 ? "err" : t.code >= 400 ? "warn" : "ok"}`}>
                      {t.code} {t.status}
                    </span>
                    <span className="traffic-path">{t.path}</span>
                    <span className="traffic-latency">{t.latency}ms</span>
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
