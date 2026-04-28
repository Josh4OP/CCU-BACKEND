from typing import List
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy import String, Boolean, Date
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .materia import Materia
    from .nota import Nota
    from .meta import Meta

class Estudiante(Base):
    __tablename__ = "estudiante"

    id_estudiante: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    correo_usuario: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True
    )

    pass_usuario: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    nombre_estudiante: Mapped[str] = mapped_column(
        String(60), nullable=False
    )

    fecha_registro: Mapped[date] = mapped_column(
    DateTime, server_default=func.now()
    )

    estado_estudiante: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    profile_pic: Mapped[str | None] = mapped_column(
        String(255), nullable=True)

    # RELACIONES
    materias: Mapped[List["Materia"]] = relationship(back_populates="estudiante")
    notas: Mapped[List["Nota"]] = relationship(back_populates="estudiante")
    metas: Mapped[List["Meta"]] = relationship(back_populates="estudiante")