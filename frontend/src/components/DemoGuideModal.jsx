import React from "react";

export default function DemoGuideModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="guide-modal" onClick={(e) => e.stopPropagation()}>
        <div className="guide-modal__header">
          <div className="guide-modal__title-box">
            <span className="guide-modal__badge">PRESENTER'S MANUAL</span>
            <h2>How to Demo Log Sentinel to Judges</h2>
          </div>
          <button className="guide-modal__close" onClick={onClose}>✕</button>
        </div>

        <div className="guide-modal__content">
          {/* Pitch Card */}
          <div className="guide-card guide-card--pitch">
            <h3>🎙️ 15-Second Pitch</h3>
            <p>
              <em>"Log Sentinel continuously monitors live production traffic through real NGINX and Microservice APIs. Using rolling Z-score statistical anomaly detection, it catches outages within 1 second, updates the live UI over WebSockets, and dispatches AWS SNS alerts."</em>
            </p>
          </div>

          {/* 4 Steps */}
          <h3 className="guide-section-title">🚀 4-Step Live Demo Flow (Click in this order)</h3>
          
          <div className="guide-steps-grid">
            <div className="guide-step-card">
              <div className="guide-step-num">STEP 1</div>
              <h4>🟢 Normal Traffic</h4>
              <p>Click <strong>"🟢 Normal Traffic"</strong> in the top bar.</p>
              <div className="guide-step-expected">
                <strong>What to tell judges:</strong> "Customers are shopping normally. NGINX processes HTTP 200 OK requests and the baseline stabilizes around 0%."
              </div>
            </div>

            <div className="guide-step-card">
              <div className="guide-step-num">STEP 2</div>
              <h4>🚨 Trigger Outage</h4>
              <p>Click <strong>"🚨 Stripe Outage (504)"</strong> or <strong>"💥 DB Deadlock"</strong>.</p>
              <div className="guide-step-expected">
                <strong>What to tell judges:</strong> "Payment API fails. The engine detects the statistical spike instantly, flips status to <strong>CRITICAL</strong>, and fires an AWS alert."
              </div>
            </div>

            <div className="guide-step-card">
              <div className="guide-step-num">STEP 3</div>
              <h4>🔄 Self-Healing Recovery</h4>
              <p>Click <strong>"🔄 Recover"</strong>.</p>
              <div className="guide-step-expected">
                <strong>What to tell judges:</strong> "As healthy traffic resumes, the sliding window flushes errors and displays <strong>SYSTEM RECOVERED</strong> without a page refresh."
              </div>
            </div>

            <div className="guide-step-card">
              <div className="guide-step-num">STEP 4</div>
              <h4>💳 Live Request</h4>
              <p>Click <strong>"💳 Send Live Checkout"</strong>.</p>
              <div className="guide-step-expected">
                <strong>What to tell judges:</strong> "This is not fake data. Every click sends an actual TCP HTTP request to our real NGINX server on port 8080."
              </div>
            </div>
          </div>

          {/* Architecture Ports */}
          <div className="guide-card guide-card--ports">
            <h4>🌐 Live Architecture & Running Ports</h4>
            <div className="guide-ports-list">
              <div className="guide-port-item">
                <span className="port-badge">Port 8080</span>
                <span><strong>Real NGINX Server:</strong> Reverse-proxies traffic and writes access logs</span>
              </div>
              <div className="guide-port-item">
                <span className="port-badge">Port 5001</span>
                <span><strong>E-Commerce Microservice:</strong> Real API (/api/products, /api/payments)</span>
              </div>
              <div className="guide-port-item">
                <span className="port-badge">Port 8000</span>
                <span><strong>Sentinel Backend:</strong> Tailer, Anomaly Engine, WebSocket & AWS Publisher</span>
              </div>
              <div className="guide-port-item">
                <span className="port-badge">Port 5173</span>
                <span><strong>React Dashboard:</strong> Live WebSocket visualizer (This UI)</span>
              </div>
            </div>
          </div>
        </div>

        <div className="guide-modal__footer">
          <button className="guide-btn-primary" onClick={onClose}>
            Got it, let's demo! 🚀
          </button>
        </div>
      </div>
    </div>
  );
}
