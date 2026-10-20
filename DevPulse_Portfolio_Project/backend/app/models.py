from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def now_utc():
    return datetime.now(timezone.utc)

class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    environment: Mapped[str] = mapped_column(String(30), default="production")
    status: Mapped[str] = mapped_column(String(20), default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    checks: Mapped[list["HealthCheck"]] = relationship(back_populates="service", cascade="all, delete-orphan")
    incidents: Mapped[list["Incident"]] = relationship(back_populates="service", cascade="all, delete-orphan")

class HealthCheck(Base):
    __tablename__ = "health_checks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, default=0)
    message: Mapped[str] = mapped_column(String(250), default="")
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    service: Mapped["Service"] = relationship(back_populates="checks")

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="major")
    status: Mapped[str] = mapped_column(String(20), default="open")
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    service: Mapped["Service"] = relationship(back_populates="incidents")
