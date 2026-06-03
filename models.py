from pydantic import model_validator
from atributos.ProgramaEstudio import Carrera
from atributos.categoriaImplemento import Categoria
from email.policy import default
from typing import Optional
from sqlmodel import SQLModel, Field
from zoneinfo import ZoneInfo
from datetime import datetime
from sqlalchemy import text, DateTime

class EstudianteBase(SQLModel):
    nombre: str = Field(default=None, min_length=1, max_length=50)
    programa: Carrera = Field(default=None, min_length=1, max_length=50)
    codigo: int = Field(default=None, gt=0)
    imagen: str | None = Field(default=None)

class EstudianteId(EstudianteBase, table=True):
    id: int = Field(default=None, primary_key=True, gt=0)
    activo: bool = True

class EstudianteUpdate(EstudianteBase):
    nombre: str = Field(default=None, min_length=1, max_length=50)
    programa: Carrera = Field(default=None, min_length=1, max_length=50)
    imagen: str | None = Field(default=None)

class ImplementoBase(SQLModel):
    nombre: str = Field(default=None, min_length=1, max_length=50)
    codigo: int = Field(default=None, gt=0)
    categoria: Categoria = Field(default=None, min_length=1, max_length=50)
    imagen: str | None = Field(default=None)


class ImplementoId(ImplementoBase, table=True):
    id: int = Field(default=None, primary_key=True, gt=0)
    activo: bool = True

class ImplementoUpdate(ImplementoBase):
    nombre: str = Field(default=None, min_length=1, max_length=50)
    categoria: Categoria = Field(default=None, min_length=1, max_length=50)
    imagen: str | None = Field(default=None)

class TurnoBase(SQLModel):
    estudiante_id: int = Field(foreign_key="estudianteid.id")
    implemento_id: int = Field(foreign_key="implementoid.id")
    codigo: int = Field(default=None, gt=0)
    activo: bool = True

class TurnoId(TurnoBase, table=True):
    id: int = Field(default=None, primary_key=True, gt=0)
    hora_inicio: datetime = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(ZoneInfo("America/Bogota")).replace(tzinfo=None),
        sa_column_kwargs={"server_default": text("CAST(timezone('America/Bogota', NOW()) AS TIMESTAMP)")}
    )

class TurnoCreate(TurnoBase):
    pass

class TurnoUpdate(SQLModel):
    estudiante_id: int = Field(foreign_key="estudianteid.id")
    implemento_id: int = Field(foreign_key="implementoid.id")