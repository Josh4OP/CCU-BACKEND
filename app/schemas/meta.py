from pydantic import BaseModel, Field

class MetaCreate(BaseModel):
    id_meta: str
    id_materia: str
    id_estudiante: int
    nota_objetivo: float = Field(..., ge=0.0, le=5.0)

class MetaUpdate(BaseModel):
    nota_objetivo: float | None = Field(default=None, ge=0.0, le=5.0)

class MetaOut(BaseModel):
    id_meta: str
    id_materia: str
    id_estudiante: int
    nota_objetivo: float

    class Config:
        from_attributes = True