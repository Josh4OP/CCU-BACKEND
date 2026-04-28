from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from app.models.estudiante import Estudiante
from app.utils.jwt import verify_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("sub")

    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == user_id
    ).first()

    if not estudiante:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return estudiante