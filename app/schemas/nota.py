from pydantic import BaseModel, Field

class NotaCreate(BaseModel):
    id_evento: str
    id_estudiante: int
    nota_obtenida: float = Field(..., ge=0.0, le=5.0)

class NotaUpdate(BaseModel):
    nota_obtenida: float = Field(..., ge=0.0, le=5.0)

class NotaOut(BaseModel):
    id_evento: str
    id_estudiante: int
    nota_obtenida: float

    class Config:
        from_attributes = True