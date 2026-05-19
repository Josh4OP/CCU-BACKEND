from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from app.models.materia import Materia
from app.models.estudiante import Estudiante
from app.schemas.materia import MateriaCreate, MateriaUpdate, MateriaOut

router = APIRouter(prefix="/materias", tags=["Materias"])


# CREAR MATERIA
@router.post("/", response_model=MateriaOut)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == materia.id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    existe = db.query(Materia).filter(
        Materia.id_materia == materia.id_materia
    ).first()
    if existe:
        return JSONResponse(status_code=400, content={"message": "Ya existe una materia con ese ID"})

    nueva_materia = Materia(**materia.model_dump())
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia


# OBTENER TODAS LAS MATERIAS
@router.get("/", response_model=list[MateriaOut])
def obtener_materias(db: Session = Depends(get_db)):
    return db.query(Materia).all()


# OBTENER MATERIAS POR ESTUDIANTE
@router.get("/estudiante/{id_estudiante}", response_model=list[MateriaOut])
def obtener_materias_por_estudiante(id_estudiante: str, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    return db.query(Materia).filter(
        Materia.id_estudiante == id_estudiante
    ).all()


# OBTENER MATERIAS POR ESTUDIANTE Y SEMESTRE
@router.get("/estudiante/{id_estudiante}/semestre/{semestre}", response_model=list[MateriaOut])
def obtener_materias_por_semestre(id_estudiante: str, semestre: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    return db.query(Materia).filter(
        Materia.id_estudiante == id_estudiante,
        Materia.semestre_materia == semestre
    ).all()


# OBTENER MATERIAS ACTIVAS POR ESTUDIANTE
@router.get("/estudiante/{id_estudiante}/activas", response_model=list[MateriaOut])
def obtener_materias_activas(id_estudiante: str, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    return db.query(Materia).filter(
        Materia.id_estudiante == id_estudiante,
        Materia.estado_materia == True
    ).all()


# OBTENER UNA MATERIA ESPECÍFICA
@router.get("/{id_materia}", response_model=MateriaOut)
def obtener_materia(id_materia: str, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})
    return materia


# ACTUALIZAR MATERIA
@router.put("/{id_materia}", response_model=MateriaOut)
def actualizar_materia(id_materia: str, datos: MateriaUpdate, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(materia, campo, valor)

    db.commit()
    db.refresh(materia)
    return materia


# CAMBIAR ESTADO DE MATERIA (activa/inactiva)
@router.patch("/{id_materia}/estado", response_model=MateriaOut)
def cambiar_estado_materia(id_materia: str, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    materia.estado_materia = not materia.estado_materia
    db.commit()
    db.refresh(materia)
    return materia


# ELIMINAR MATERIA
@router.delete("/{id_materia}")
def eliminar_materia(id_materia: str, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    db.delete(materia)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Materia eliminada correctamente"})