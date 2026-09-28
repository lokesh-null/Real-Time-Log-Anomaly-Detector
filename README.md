# Real-Time Log Anomaly Detector Backend

This is the backend component for the Real-Time Log Anomaly Detector, providing the core integration layer, WebSocket management, log monitoring, and routing.

## Architecture

The backend behaves as the central integration spine connecting:
- Tejeshwar's log generation simulator
- Lokesh's FastAPI backend (this service)
- Jashwanth's Anomaly Detection Engine
- Harish's React Dashboard

### Data Flow
1. The backend continuously tails `logs/app.log`.
2. As new logs are written by the simulator, they are parsed asynchronously into structured models.
3. Structured logs are passed into the Anomaly Detector adapter.
4. The detector responds with an `AnomalyResult` which contains metrics (error rate, baseline, deviation) and severity classification.
5. The backend broadcasts the results to connected frontend clients via WebSocket.
6. The backend pushes critical alerts to AWS SNS (via the Alert Publisher adapter).

## Setup & Installation

### Requirements
- Python 3.9+

### Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Copy the provided `.env.example` to `.env` and configure accordingly:
```bash
LOG_FILE_PATH=logs/app.log
POLL_INTERVAL=0.2
AWS_REGION=us-east-1
SNS_TOPIC_ARN=
```

## Running the Application

```bash
uvicorn backend.main:app --reload
```
The server will start on `http://127.0.0.1:8000`.

## Endpoints

- **GET `/health`**: Returns the health status and number of connected WebSocket clients.
- **WS `/ws`**: WebSocket endpoint for frontend connection to receive live metric updates.

## Integrations

- **Jashwanth**: Implement the core anomaly detection logic inside `backend/services/detector_adapter.py`.
- **Tejeshwar**: Implement the AWS SNS publishing inside `backend/services/alert_publisher.py`.
- **Harish**: Connect to `ws://localhost:8000/ws` for real-time JSON metrics updates to power the dashboard.

## Development & Testing

Run tests with `pytest`:
```bash
pytest tests/
```
