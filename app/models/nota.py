from typing import List
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,ForeignKey, Boolean, Date
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .estudiante import Estudiante
    from .evento_evaluativo import EventoEvaluativo

class Nota(Base):
    __tablename__ = "nota"

    id_evento: Mapped[str] = mapped_column(
        ForeignKey("evento_evaluativo.id_evento"),
        primary_key=True
    )

    id_estudiante: Mapped[str] = mapped_column(
        ForeignKey("estudiante.id_estudiante"),
        primary_key=True
    )

    nota_obtenida: Mapped[float]

    estudiante: Mapped["Estudiante"] = relationship(back_populates="notas")

    evento: Mapped["EventoEvaluativo"] = relationship(back_populates="notas")