from typing import List
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey,Boolean, Date
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .materia import Materia
    from .nota import Nota




class EventoEvaluativo(Base):
    __tablename__ = "evento_evaluativo"

    id_evento: Mapped[str] = mapped_column(String(60), primary_key=True)

    id_materia: Mapped[str] = mapped_column(
        ForeignKey("materia.id_materia")
    )

    titulo_evento: Mapped[str]

    desc_evento: Mapped[str]

    fecha_evento: Mapped[date]

    prioridad_evento: Mapped[int]

    pond_evento: Mapped[float]

    corte_evento: Mapped[int]

    estado_evento: Mapped[bool]

    materia: Mapped["Materia"] = relationship(back_populates="eventos")

    notas: Mapped[list["Nota"]] = relationship(back_populates="evento")