/**
 * Mock data generator for frontend-only development/testing.
 * Follows the exact shared data contract agreed with the backend team.
 *
 * Schema:
 * {
 *   timestamp, error_rate, baseline, deviation,
 *   severity, is_anomaly, message, errors, total_logs
 * }
 */

const MOCK_SEQUENCE = [
  // Normal operation
  { error_rate: 0.03, baseline: 0.05, deviation: 0.4, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 3, total_logs: 100 },
  { error_rate: 0.04, baseline: 0.05, deviation: 0.6, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 4, total_logs: 100 },
  { error_rate: 0.05, baseline: 0.05, deviation: 0.2, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 5, total_logs: 100 },
  { error_rate: 0.06, baseline: 0.05, deviation: 0.8, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 6, total_logs: 100 },
  { error_rate: 0.04, baseline: 0.05, deviation: 0.3, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 4, total_logs: 100 },
  // Climbing
  { error_rate: 0.09, baseline: 0.05, deviation: 1.5, severity: "NORMAL", is_anomaly: false, message: "Error rate slightly elevated", errors: 9, total_logs: 100 },
  { error_rate: 0.12, baseline: 0.06, deviation: 2.1, severity: "WARNING", is_anomaly: true, message: "Error rate above baseline", errors: 12, total_logs: 100 },
  { error_rate: 0.18, baseline: 0.06, deviation: 2.8, severity: "WARNING", is_anomaly: true, message: "Error rate elevated — monitoring", errors: 18, total_logs: 100 },
  { error_rate: 0.25, baseline: 0.06, deviation: 3.5, severity: "HIGH", is_anomaly: true, message: "Significant error rate deviation detected", errors: 25, total_logs: 100 },
  { error_rate: 0.34, baseline: 0.07, deviation: 4.2, severity: "HIGH", is_anomaly: true, message: "Error rate significantly above baseline", errors: 34, total_logs: 100 },
  // Critical spike
  { error_rate: 0.48, baseline: 0.07, deviation: 5.8, severity: "CRITICAL", is_anomaly: true, message: "Error rate exceeded baseline", errors: 48, total_logs: 100 },
  { error_rate: 0.61, baseline: 0.07, deviation: 7.2, severity: "CRITICAL", is_anomaly: true, message: "CRITICAL: Error rate spike detected", errors: 61, total_logs: 100 },
  { error_rate: 0.55, baseline: 0.08, deviation: 6.5, severity: "CRITICAL", is_anomaly: true, message: "Error rate remains critically elevated", errors: 55, total_logs: 100 },
  // Recovery
  { error_rate: 0.38, baseline: 0.08, deviation: 4.0, severity: "HIGH", is_anomaly: true, message: "Error rate decreasing", errors: 38, total_logs: 100 },
  { error_rate: 0.22, baseline: 0.08, deviation: 2.6, severity: "WARNING", is_anomaly: true, message: "Error rate trending toward baseline", errors: 22, total_logs: 100 },
  { error_rate: 0.10, baseline: 0.07, deviation: 1.2, severity: "NORMAL", is_anomaly: false, message: "System returned to normal operating range", errors: 10, total_logs: 100 },
  { error_rate: 0.06, baseline: 0.07, deviation: 0.3, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 6, total_logs: 100 },
  { error_rate: 0.05, baseline: 0.06, deviation: 0.2, severity: "NORMAL", is_anomaly: false, message: "System operating normally", errors: 5, total_logs: 100 },
];

let index = 0;

/**
 * Returns the next mock event in the realistic sequence.
 * Cycles through the full NORMAL → CRITICAL → RECOVERED loop.
 */
export function getNextMockEvent() {
  const template = MOCK_SEQUENCE[index % MOCK_SEQUENCE.length];
  index++;

  return {
    ...template,
    timestamp: new Date().toISOString(),
  };
}

/**
 * Resets the mock sequence index (useful for testing).
 */
export function resetMockSequence() {
  index = 0;
}
