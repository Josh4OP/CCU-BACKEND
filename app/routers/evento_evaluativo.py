from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from app.models.evento_evaluativo import EventoEvaluativo
from app.models.materia import Materia
from app.schemas.evento_evaluativo import (
    EventoEvaluativoCreate,
    EventoEvaluativoUpdate,
    EventoEvaluativoOut
)

router = APIRouter(prefix="/eventos", tags=["Eventos Evaluativos"])


# CREAR EVENTO
@router.post("/", response_model=EventoEvaluativoOut)
def crear_evento(evento: EventoEvaluativoCreate, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == evento.id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    existe = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == evento.id_evento
    ).first()
    if existe:
        return JSONResponse(status_code=400, content={"message": "Ya existe un evento con ese ID"})

    nuevo_evento = EventoEvaluativo(**evento.model_dump())
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento


# OBTENER TODOS LOS EVENTOS
@router.get("/", response_model=list[EventoEvaluativoOut])
def obtener_eventos(db: Session = Depends(get_db)):
    return db.query(EventoEvaluativo).all()


# OBTENER EVENTOS POR MATERIA
@router.get("/materia/{id_materia}", response_model=list[EventoEvaluativoOut])
def obtener_eventos_por_materia(id_materia: str, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    return db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_materia == id_materia
    ).all()


# OBTENER EVENTOS POR CORTE
@router.get("/materia/{id_materia}/corte/{corte}", response_model=list[EventoEvaluativoOut])
def obtener_eventos_por_corte(id_materia: str, corte: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(
        Materia.id_materia == id_materia
    ).first()
    if not materia:
        return JSONResponse(status_code=404, content={"message": "Materia no encontrada"})

    return db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_materia == id_materia,
        EventoEvaluativo.corte_evento == corte
    ).all()


# OBTENER UN EVENTO ESPECÍFICO
@router.get("/{id_evento}", response_model=EventoEvaluativoOut)
def obtener_evento(id_evento: str, db: Session = Depends(get_db)):
    evento = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == id_evento
    ).first()
    if not evento:
        return JSONResponse(status_code=404, content={"message": "Evento no encontrado"})
    return evento


# ACTUALIZAR EVENTO
@router.put("/{id_evento}", response_model=EventoEvaluativoOut)
def actualizar_evento(id_evento: str, datos: EventoEvaluativoUpdate, db: Session = Depends(get_db)):
    evento = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == id_evento
    ).first()
    if not evento:
        return JSONResponse(status_code=404, content={"message": "Evento no encontrado"})

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(evento, campo, valor)

    db.commit()
    db.refresh(evento)
    return evento


# CAMBIAR ESTADO DEL EVENTO (activo/inactivo)
@router.patch("/{id_evento}/estado", response_model=EventoEvaluativoOut)
def cambiar_estado_evento(id_evento: str, db: Session = Depends(get_db)):
    evento = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == id_evento
    ).first()
    if not evento:
        return JSONResponse(status_code=404, content={"message": "Evento no encontrado"})

    evento.estado_evento = not evento.estado_evento
    db.commit()
    db.refresh(evento)
    return evento


# ELIMINAR EVENTO
@router.delete("/{id_evento}")
def eliminar_evento(id_evento: str, db: Session = Depends(get_db)):
    evento = db.query(EventoEvaluativo).filter(
        EventoEvaluativo.id_evento == id_evento
    ).first()
    if not evento:
        return JSONResponse(status_code=404, content={"message": "Evento no encontrado"})

    db.delete(evento)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Evento eliminado correctamente"})