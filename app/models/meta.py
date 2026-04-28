from typing import List
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,ForeignKey, Boolean, Date
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .estudiante import Estudiante
    from .materia import Materia

class Meta(Base):
    __tablename__ = "meta"

    id_meta: Mapped[str] = mapped_column(String(60), primary_key=True)

    id_materia: Mapped[str] = mapped_column(
        ForeignKey("materia.id_materia")
    )

    id_estudiante: Mapped[str] = mapped_column(
        ForeignKey("estudiante.id_estudiante")
    )

    nota_objetivo: Mapped[float]

    estudiante: Mapped["Estudiante"] = relationship(back_populates="metas")

    materia: Mapped["Materia"] = relationship(back_populates="metas")