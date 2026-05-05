from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ✅ BASE (campos comunes)
class EstudianteBase(BaseModel):
    nombre: str
    correo: EmailStr


# ✅ REGISTRO
class EstudianteCreate(EstudianteBase):
    password: str


# ✅ LOGIN
class EstudianteLogin(BaseModel):
    correo: EmailStr
    password: str


# ✅ RESPUESTA (lo que devuelves)
class EstudianteOut(BaseModel):
    id_estudiante: int
    nombre_estudiante: str
    correo_usuario: EmailStr
    fecha_registro: datetime
    estado_estudiante: bool
    profile_pic: Optional[str]

    class Config:
        from_attributes = True   # 👈 necesario para SQLAlchemy

class CambiarPassword(BaseModel):
    correo: EmailStr
    password_actual: str
    password_nueva: str