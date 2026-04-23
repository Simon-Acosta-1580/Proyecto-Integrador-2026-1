from pydantic import BaseModel, Field
from ProgramaEstudio import Carrera
from categoriaImplemento import Categoria
from typing import Optional

class EstudianteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    programa: Carrera = Field(..., min_length=1, max_length=50)
    codigo: int = Field(..., gt=0)

class EstudianteId(EstudianteBase):
    id: int = Field(..., gt=0)

class ImplementoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    categoria: Categoria = Field(..., min_length=1, max_length=50)

class ImplementoId(ImplementoBase):
    id: int = Field(..., gt=0)