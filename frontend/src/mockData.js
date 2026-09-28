/**
 * Mock data generator — exact backend contract.
 * Produces a realistic NORMAL→CRITICAL→RECOVERED cycle.
 * Also produces raw log entries for the console view.
 */

const SEQUENCE = [
  { error_rate: 0.03, baseline: 0.05, deviation: 0.4, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 3, total_logs: 100 },
  { error_rate: 0.04, baseline: 0.05, deviation: 0.6, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 4, total_logs: 108 },
  { error_rate: 0.05, baseline: 0.05, deviation: 0.2, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 5, total_logs: 115 },
  { error_rate: 0.06, baseline: 0.05, deviation: 0.8, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 6, total_logs: 122 },
  { error_rate: 0.04, baseline: 0.05, deviation: 0.3, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 4, total_logs: 130 },
  { error_rate: 0.09, baseline: 0.05, deviation: 1.5, severity: "NORMAL", is_anomaly: false, message: "Error rate slightly elevated", errors: 9, total_logs: 140 },
  { error_rate: 0.12, baseline: 0.06, deviation: 2.1, severity: "WARNING", is_anomaly: true, message: "Error rate above baseline", errors: 15, total_logs: 148 },
  { error_rate: 0.18, baseline: 0.06, deviation: 2.8, severity: "WARNING", is_anomaly: true, message: "Error rate elevated — monitoring", errors: 22, total_logs: 155 },
  { error_rate: 0.25, baseline: 0.06, deviation: 3.5, severity: "HIGH", is_anomaly: true, message: "Significant error rate deviation detected", errors: 30, total_logs: 162 },
  { error_rate: 0.34, baseline: 0.07, deviation: 4.2, severity: "HIGH", is_anomaly: true, message: "Error rate significantly above baseline", errors: 38, total_logs: 170 },
  { error_rate: 0.48, baseline: 0.07, deviation: 5.8, severity: "CRITICAL", is_anomaly: true, message: "Error rate exceeded baseline", errors: 50, total_logs: 178 },
  { error_rate: 0.61, baseline: 0.07, deviation: 7.2, severity: "CRITICAL", is_anomaly: true, message: "CRITICAL: Error rate spike detected", errors: 65, total_logs: 185 },
  { error_rate: 0.55, baseline: 0.08, deviation: 6.5, severity: "CRITICAL", is_anomaly: true, message: "Error rate remains critically elevated", errors: 58, total_logs: 190 },
  { error_rate: 0.38, baseline: 0.08, deviation: 4.0, severity: "HIGH", is_anomaly: true, message: "Error rate decreasing", errors: 42, total_logs: 198 },
  { error_rate: 0.22, baseline: 0.08, deviation: 2.6, severity: "WARNING", is_anomaly: true, message: "Error rate trending toward baseline", errors: 28, total_logs: 205 },
  { error_rate: 0.10, baseline: 0.07, deviation: 1.2, severity: "NORMAL", is_anomaly: false, message: "System returned to normal operating range", errors: 12, total_logs: 212 },
  { error_rate: 0.06, baseline: 0.07, deviation: 0.3, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 7, total_logs: 220 },
  { error_rate: 0.05, baseline: 0.06, deviation: 0.2, severity: "NORMAL", is_anomaly: false, message: "System operating within baseline", errors: 6, total_logs: 228 },
];

const LOG_MESSAGES = [
  { level: "INFO", message: "Request received GET /api/users" },
  { level: "INFO", message: "Request processed in 42ms" },
  { level: "INFO", message: "Database query executed successfully" },
  { level: "DEBUG", message: "Cache hit for key user:1234" },
  { level: "INFO", message: "Request received POST /api/orders" },
  { level: "WARNING", message: "Slow query detected: 1250ms" },
  { level: "INFO", message: "Request received GET /api/health" },
  { level: "ERROR", message: "Database connection failed: timeout" },
  { level: "ERROR", message: "500 Internal Server Error: NullPointerException" },
  { level: "CRITICAL", message: "Connection pool exhausted" },
  { level: "INFO", message: "Retry succeeded after 3 attempts" },
  { level: "WARNING", message: "Memory usage above 80%" },
  { level: "ERROR", message: "Service unavailable: payment-gateway" },
  { level: "INFO", message: "Health check passed" },
  { level: "INFO", message: "Request received DELETE /api/sessions/expired" },
];

let idx = 0;
let logIdx = 0;

export function getNextMockEvent() {
  const t = SEQUENCE[idx % SEQUENCE.length];
  idx++;
  return { ...t, timestamp: new Date().toISOString() };
}

export function getNextMockLog() {
  const entry = LOG_MESSAGES[logIdx % LOG_MESSAGES.length];
  logIdx++;
  return {
    timestamp: new Date().toISOString(),
    level: entry.level,
    message: entry.message,
  };
}

export function resetMock() {
  idx = 0;
  logIdx = 0;
}
