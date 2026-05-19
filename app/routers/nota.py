from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from app.models.nota import Nota
from app.models.estudiante import Estudiante
from app.models.evento_evaluativo import EventoEvaluativo
from app.schemas.nota import NotaCreate, NotaOut, NotaUpdate
router = APIRouter(prefix="/notas", tags=["Notas"])


# REGISTRAR NOTA
@router.post("/", response_model=NotaOut)
def registrar_nota(nota: NotaCreate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == nota.id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    evento = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == nota.id_evento
    ).first()
    if not evento:
        return JSONResponse(status_code=404, content={"message": "Evento evaluativo no encontrado"})

    existe = db.query(Nota).filter(
        Nota.id_evento == nota.id_evento,
        Nota.id_estudiante == nota.id_estudiante
    ).first()
    if existe:
        return JSONResponse(status_code=400, content={"message": "Ya existe una nota para este estudiante en este evento"})

    nueva_nota = Nota(
        id_evento=nota.id_evento,
        id_estudiante=nota.id_estudiante,
        nota_obtenida=nota.nota_obtenida
    )
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota


# OBTENER TODAS LAS NOTAS
@router.get("/", response_model=list[NotaOut])
def obtener_notas(db: Session = Depends(get_db)):
    return db.query(Nota).all()


# OBTENER NOTAS POR ESTUDIANTE
@router.get("/estudiante/{id_estudiante}", response_model=list[NotaOut])
def obtener_notas_por_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == id_estudiante
    ).first()
    if not estudiante:
        return JSONResponse(status_code=404, content={"message": "Estudiante no encontrado"})

    notas = db.query(Nota).filter(Nota.id_estudiante == id_estudiante).all()
    return notas


# OBTENER NOTAS POR EVENTO
@router.get("/evento/{id_evento}", response_model=list[NotaOut])
def obtener_notas_por_evento(id_evento: str, db: Session = Depends(get_db)):
    evento = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == id_evento
    ).first()
    if not evento:
        return JSONResponse(status_code=404, content={"message": "Evento evaluativo no encontrado"})

    notas = db.query(Nota).filter(Nota.id_evento == id_evento).all()
    return notas


# OBTENER UNA NOTA ESPECÍFICA (PK compuesta)
@router.get("/{id_evento}/{id_estudiante}", response_model=NotaOut)
def obtener_nota(id_evento: str, id_estudiante: int, db: Session = Depends(get_db)):
    nota = db.query(Nota).filter(
        Nota.id_evento == id_evento,
        Nota.id_estudiante == id_estudiante
    ).first()
    if not nota:
        return JSONResponse(status_code=404, content={"message": "Nota no encontrada"})
    return nota


# ACTUALIZAR NOTA
@router.put("/{id_evento}/{id_estudiante}", response_model=NotaOut)
def actualizar_nota(id_evento: str, id_estudiante: int, datos: NotaUpdate, db: Session = Depends(get_db)):
    nota = db.query(Nota).filter(
        Nota.id_evento == id_evento,
        Nota.id_estudiante == id_estudiante
    ).first()
    if not nota:
        return JSONResponse(status_code=404, content={"message": "Nota no encontrada"})

    nota.nota_obtenida = datos.nota_obtenida
    db.commit()
    db.refresh(nota)
    return nota


# ELIMINAR NOTA
@router.delete("/{id_evento}/{id_estudiante}")
def eliminar_nota(id_evento: str, id_estudiante: int, db: Session = Depends(get_db)):
    nota = db.query(Nota).filter(
        Nota.id_evento == id_evento,
        Nota.id_estudiante == id_estudiante
    ).first()
    if not nota:
        return JSONResponse(status_code=404, content={"message": "Nota no encontrada"})

    db.delete(nota)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Nota eliminada correctamente"})