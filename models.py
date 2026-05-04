from pydantic import BaseModel, Field, model_validator
from atributos.ProgramaEstudio import Carrera
from atributos.categoriaImplemento import Categoria
from atributos.horarioTurno import Horario


class EstudianteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    programa: Carrera = Field(..., min_length=1, max_length=50)
    codigo: int = Field(..., gt=0)
    activo: bool = True

class EstudianteId(EstudianteBase):
    id: int = Field(..., gt=0)

class ImplementoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    codigo: int = Field(..., gt=0)
    categoria: Categoria = Field(..., min_length=1, max_length=50)
    activo: bool = True

class ImplementoId(ImplementoBase):
    id: int = Field(..., gt=0)

class TurnoBase(BaseModel):
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
