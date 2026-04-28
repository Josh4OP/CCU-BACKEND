from typing import List
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean, Date
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .estudiante import Estudiante
    from .evento_evaluativo import EventoEvaluativo
    from .meta import Meta


class Materia(Base):
    __tablename__ = "materia"

    id_materia: Mapped[str] = mapped_column(String(60), primary_key=True)

    id_estudiante: Mapped[str] = mapped_column(
        ForeignKey("estudiante.id_estudiante")
    )

    nombre_materia: Mapped[str] = mapped_column(String(100), nullable=False)

    profesor_materia: Mapped[str] = mapped_column(String(100))

    credito_materia: Mapped[float]

    semestre_materia: Mapped[int]

    estado_materia: Mapped[bool] = mapped_column(Boolean)

    estudiante: Mapped["Estudiante"] = relationship(back_populates="materias")

    eventos: Mapped[list["EventoEvaluativo"]] = relationship(
        back_populates="materia"
    )

    metas: Mapped[list["Meta"]] = relationship(back_populates="materia")