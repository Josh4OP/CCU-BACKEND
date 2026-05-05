from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from app.models.estudiante import Estudiante
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.utils.deps import get_current_user
from app.schemas.estudiante import *
import os, shutil
from app.schemas.estudiante import CambiarPassword  # schema nuevo


router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

UPLOAD_DIR = os.path.join("uploads", "profile_pics")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ REGISTRO
@router.post("/register", response_model=EstudianteOut)
def register(estudiante: EstudianteCreate, db: Session = Depends(get_db)):

    existe = db.query(Estudiante).filter(
        Estudiante.correo_usuario == estudiante.correo
    ).first()

    if existe:
        return JSONResponse(status_code=400, content={"message": "El correo ya existe"})

    nuevo = Estudiante(
        nombre_estudiante=estudiante.nombre,
        correo_usuario=estudiante.correo,
        pass_usuario=hash_password(estudiante.password)
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ✅ LOGIN
@router.post("/login")
def login(data: EstudianteLogin, db: Session = Depends(get_db)):

    estudiante = db.query(Estudiante).filter(
        Estudiante.correo_usuario == data.correo
    ).first()

    if not estudiante:
        return JSONResponse(status_code=401, content={"message": "Credenciales incorrectas"})

    if not verify_password(data.password, estudiante.pass_usuario):
        return JSONResponse(status_code=401, content={"message": "Credenciales incorrectas"})

    token = create_access_token({
        "sub": str(estudiante.id_estudiante)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ✅ LISTAR
@router.get("/", response_model=list[EstudianteOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()


# ✅ OBTENER
@router.get("/{id}", response_model=EstudianteOut)
def obtener(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id
    ).first()

    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})

    return estudiante

@router.get("/me")
def perfil(usuario = Depends(get_current_user)):
    return usuario

# ✅ SUBIR FOTO
@router.post("/upload-profile-pic/{id}")
def upload_pic(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id
    ).first()

    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})

    filename = f"user_{id}{os.path.splitext(file.filename)[1]}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    estudiante.profile_pic = f"/uploads/profile_pics/{filename}"
    db.commit()

    return {"message": "Foto actualizada", "url": estudiante.profile_pic}

@router.put("/change-password")
def change_password(data: CambiarPassword, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.correo_usuario == data.correo
    ).first()
    if not estudiante or not verify_password(data.password_actual, estudiante.pass_usuario):
        return JSONResponse(status_code=401, content={"message": "Contraseña actual incorrecta"})
    estudiante.pass_usuario = hash_password(data.password_nueva)
    db.commit()
    return {"message": "Contraseña actualizada correctamente."}