from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import Base, engine, get_db, SessionLocal
from .models import Service, HealthCheck, Incident
from .schemas import ServiceCreate, ServiceOut, CheckCreate, CheckOut, IncidentOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Service).count() == 0:
            service = Service(name="Example Payments API", url="https://payments.example.com", environment="production", status="up")
            db.add(service)
            db.flush()
            db.add(HealthCheck(service_id=service.id, status="up", latency_ms=84, message="Demo check passed"))
            db.commit()
    finally:
        db.close()
    yield

app = FastAPI(title="DevPulse API", version="1.0.0", description="Service health and incident tracking API.", lifespan=lifespan)

@app.get("/api/health", tags=["System"])
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/api/services", response_model=list[ServiceOut], tags=["Services"])
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).order_by(Service.id).all()

@app.post("/api/services", response_model=ServiceOut, status_code=201, tags=["Services"])
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    url = str(payload.url).rstrip("/")
    if db.query(Service).filter(Service.url == url).first():
        raise HTTPException(status_code=409, detail="A service with this URL already exists.")
    item = Service(name=payload.name.strip(), url=url, environment=payload.environment, status="unknown")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/api/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Services"])
def delete_service(service_id: int, db: Session = Depends(get_db)):
    item = db.get(Service, service_id)
    if not item:
        raise HTTPException(status_code=404, detail="Service not found.")
    db.delete(item)
    db.commit()

@app.post("/api/services/{service_id}/checks", response_model=CheckOut, status_code=201, tags=["Health checks"])
def create_check(service_id: int, payload: CheckCreate, db: Session = Depends(get_db)):
    item = db.get(Service, service_id)
    if not item:
        raise HTTPException(status_code=404, detail="Service not found.")
    check = HealthCheck(service_id=service_id, status=payload.status, latency_ms=payload.latency_ms, message=payload.message)
    item.status = payload.status
    db.add(check)
    if payload.status == "down":
        exists = db.query(Incident).filter(Incident.service_id == service_id, Incident.status == "open").first()
        if not exists:
            db.add(Incident(service_id=service_id, title=f"{item.name} is down", severity="critical",
                            status="open", details=payload.message or "A health check reported the service as down."))
    db.commit()
    db.refresh(check)
    return check

@app.get("/api/incidents", response_model=list[IncidentOut], tags=["Incidents"])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(desc(Incident.created_at)).all()

@app.patch("/api/incidents/{incident_id}/resolve", response_model=IncidentOut, tags=["Incidents"])
def resolve_incident(incident_id: int, db: Session = Depends(get_db)):
    item = db.get(Incident, incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found.")
    item.status = "resolved"
    item.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/dashboard", tags=["Dashboard"])
def dashboard(db: Session = Depends(get_db)):
    services = db.query(Service).order_by(Service.id).all()
    incidents = db.query(Incident).order_by(desc(Incident.created_at)).limit(8).all()
    checks = db.query(HealthCheck).all()
    uptime = round(sum(c.status == "up" for c in checks) * 100 / len(checks), 1) if checks else 100.0
    return {
        "total_services": len(services),
        "operational_services": sum(s.status == "up" for s in services),
        "open_incidents": db.query(Incident).filter(Incident.status == "open").count(),
        "uptime_percent": uptime,
        "services": [ServiceOut.model_validate(s).model_dump(mode="json") for s in services],
        "incidents": [IncidentOut.model_validate(i).model_dump(mode="json") for i in incidents],
    }
