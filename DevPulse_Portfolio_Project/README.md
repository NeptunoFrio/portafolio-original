# DevPulse — Service Health Dashboard

A portfolio project with a FastAPI REST API, SQLite persistence, and a responsive TypeScript dashboard.

## Features
- Service registry with duplicate URL validation
- Health-check history and service status updates
- Incident creation when a service is reported down
- Incident resolution workflow
- Dashboard summary metrics
- API docs at `/docs`
- Tests for core endpoints

## Requirements
Python 3.11+ and Node.js 18+.

## Run the backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000 — docs: http://127.0.0.1:8000/docs

## Run the frontend
Open another terminal:
```bash
cd frontend
npm install
npm run dev
```
Use the URL Vite prints (usually http://localhost:5173).

## Run tests
```bash
cd backend
pytest
```

## API
- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/services`
- `POST /api/services`
- `DELETE /api/services/{id}`
- `POST /api/services/{id}/checks`
- `GET /api/incidents`
- `PATCH /api/incidents/{id}/resolve`

## Honest portfolio note
The project records submitted health checks but does not yet run scheduled checks against real endpoints. A good next feature is a background scheduler, followed by authentication, alert notifications, and historical charts. Customize it and understand the code before presenting it as your work.
