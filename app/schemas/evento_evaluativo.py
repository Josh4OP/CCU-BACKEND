from pydantic import BaseModel, Field
from datetime import date

class EventoEvaluativoCreate(BaseModel):
    id_evento: str
    id_materia: str
    titulo_evento: str
    desc_evento: str
    fecha_evento: date
    prioridad_evento: int = Field(..., ge=1)
    pond_evento: float = Field(..., ge=0.0, le=100.0)
    corte_evento: int = Field(..., ge=1, le=3)
    estado_evento: bool

class EventoEvaluativoUpdate(BaseModel):
    titulo_evento: str | None = None
    desc_evento: str | None = None
    fecha_evento: date | None = None
    prioridad_evento: int | None = Field(default=None, ge=1)
    pond_evento: float | None = Field(default=None, ge=0.0, le=100.0)
    corte_evento: int | None = Field(default=None, ge=1, le=3)
    estado_evento: bool | None = None

class EventoEvaluativoOut(BaseModel):
    id_evento: str
    id_materia: str
    titulo_evento: str
    desc_evento: str
    fecha_evento: date
    prioridad_evento: int
    pond_evento: float
    corte_evento: int
    estado_evento: bool

    class Config:
        from_attributes = True