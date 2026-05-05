from pydantic import model_validator
from atributos.ProgramaEstudio import Carrera
from atributos.categoriaImplemento import Categoria
from atributos.horarioTurno import Horario
from email.policy import default
from typing import Optional
from sqlmodel import SQLModel, Field

class EstudianteBase(SQLModel):
    nombre: str = Field(default=None, min_length=1, max_length=50)
    programa: Carrera = Field(default=None, min_length=1, max_length=50)
    codigo: int = Field(default=None, gt=0)
    activo: bool = True

class EstudianteId(EstudianteBase, table=True):
    id: int = Field(default=None, primary_key=True, gt=0)

class EstudianteUpdate(EstudianteBase):
    nombre: str = Field(default=None, min_length=1, max_length=50)
    programa: Carrera = Field(default=None, min_length=1, max_length=50)
    codigo: int = Field(None, exclude=True)
    activo: bool = Field(None, exclude=True)

class ImplementoBase(SQLModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    codigo: int = Field(..., gt=0)
    categoria: Categoria = Field(..., min_length=1, max_length=50)
    activo: bool = True

class ImplementoId(ImplementoBase):
    id: int = Field(..., gt=0)

class TurnoBase(SQLModel):
    codigo: int = Field(..., gt=0)
    hora_inicio: int = Field(..., gt=8, le=19)
    horario: Horario = Field(..., min_length=1, max_length=50)
    activo: bool = True

    @model_validator(mode='after')
    def validar_horario_diurno(self):
        es_diurno = self.horario.lower() == "diurno"

        if es_diurno and self.hora_inicio >= 18:
            raise ValueError("Los turnos de tipo 'Diurno' no pueden iniciar después de las 18 horas.")

        return self

class TurnoId(TurnoBase):
    id: int = Field(..., gt=0)
