from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from app.models.meta import Meta
from app.models.materia import Materia
from app.models.estudiante import Estudiante
from app.schemas.meta import MetaCreate, MetaUpdate, MetaOut

router = APIRouter(prefix="/metas", tags=["Metas"])


# CREAR META
@router.post("/", response_model=MetaOut)
def crear_meta(meta: MetaCreate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == meta.id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    materia = db.query(Materia).filter(
        Materia.id_materia == meta.id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    # Verificar que la materia pertenece al estudiante
    if materia.id_estudiante != meta.id_estudiante:
        return JSONResponse(status_code=400, content={"message": "La materia no pertenece a este estudiante"})

    existe = db.query(Meta).filter(Meta.id_meta == meta.id_meta).first()
    if existe:
        return JSONResponse(status_code=400, content={"message": "Ya existe una meta con ese ID"})

    # Verificar que no exista ya una meta para esa materia
    meta_duplicada = db.query(Meta).filter(
        Meta.id_materia == meta.id_materia,
        Meta.id_estudiante == meta.id_estudiante
    ).first()
    if meta_duplicada:
        return JSONResponse(status_code=400, content={"message": "Ya existe una meta para esta materia"})

    nueva_meta = Meta(**meta.model_dump())
    db.add(nueva_meta)
    db.commit()
    db.refresh(nueva_meta)
    return nueva_meta


# OBTENER TODAS LAS METAS
@router.get("/", response_model=list[MetaOut])
def obtener_metas(db: Session = Depends(get_db)):
    return db.query(Meta).all()


# OBTENER METAS POR ESTUDIANTE
@router.get("/estudiante/{id_estudiante}", response_model=list[MetaOut])
def obtener_metas_por_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    return db.query(Meta).filter(Meta.id_estudiante == id_estudiante).all()


# OBTENER META POR MATERIA
@router.get("/materia/{id_materia}", response_model=MetaOut)
def obtener_meta_por_materia(id_materia: str, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id_materia == id_materia).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    meta = db.query(Meta).filter(Meta.id_materia == id_materia).first()
    if not meta:
        return JSONResponse(status_code=404, content={"message": "No hay meta definida para esta materia"})
    return meta


# OBTENER UNA META ESPECÍFICA
@router.get("/{id_meta}", response_model=MetaOut)
def obtener_meta(id_meta: str, db: Session = Depends(get_db)):
    meta = db.query(Meta).filter(Meta.id_meta == id_meta).first()
    if not meta:
        return JSONResponse(status_code=404, content={"message": "Meta no encontrada"})
    return meta


# ACTUALIZAR META
@router.put("/{id_meta}", response_model=MetaOut)
def actualizar_meta(id_meta: str, datos: MetaUpdate, db: Session = Depends(get_db)):
    meta = db.query(Meta).filter(Meta.id_meta == id_meta).first()
    if not meta:
        return JSONResponse(status_code=404, content={"message": "Meta no encontrada"})

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(meta, campo, valor)

    db.commit()
    db.refresh(meta)
    return meta


# ELIMINAR META
@router.delete("/{id_meta}")
def eliminar_meta(id_meta: str, db: Session = Depends(get_db)):
    meta = db.query(Meta).filter(Meta.id_meta == id_meta).first()
    if not meta:
        return JSONResponse(status_code=404, content={"message": "Meta no encontrada"})

    db.delete(meta)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Meta eliminada correctamente"})