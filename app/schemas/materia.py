from pydantic import BaseModel, Field

class MateriaCreate(BaseModel):
    id_materia: str
    id_estudiante: int
    nombre_materia: str
    profesor_materia: str
    credito_materia: float = Field(..., gt=0.0)
    semestre_materia: int = Field(..., ge=1)
    estado_materia: bool

class MateriaUpdate(BaseModel):
    nombre_materia: str | None = None
    profesor_materia: str | None = None
    credito_materia: float | None = Field(default=None, gt=0.0)
    semestre_materia: int | None = Field(default=None, ge=1)
    estado_materia: bool | None = None

class MateriaOut(BaseModel):
    id_materia: str
    id_estudiante: int
    nombre_materia: str
    profesor_materia: str
    credito_materia: float
    semestre_materia: int
    estado_materia: bool

    class Config:
        from_attributes = True