from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

Environment = Literal["production", "staging", "development"]
CheckStatus = Literal["up", "degraded", "down"]

class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    url: HttpUrl
    environment: Environment = "production"

class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    url: str
    environment: str
    status: str
    created_at: datetime

class CheckCreate(BaseModel):
    status: CheckStatus
    latency_ms: float = Field(default=0, ge=0, le=120000)
    message: str = Field(default="", max_length=250)

class CheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    service_id: int
    status: str
    latency_ms: float
    message: str
    checked_at: datetime

class IncidentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    service_id: int
    title: str
    severity: str
    status: str
    details: str
    created_at: datetime
    resolved_at: datetime | None
