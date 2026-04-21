from typing import List
from fastapi import FastAPI, HTTPException
from Estudiante_operations import createEstudiante, showEstudiantes, showEstudiante
from models import (EstudianteBase, EstudianteId)

app = FastAPI()

@app.get("/hola")
def hola():
    return {"message": "Hello World"}

@app.post("/estudiante", response_model=EstudianteId)
async def create_estudiante(pokemon:EstudianteBase):
    return createEstudiante(pokemon)

@app.get("/estudiante", response_model=list[EstudianteId])
async def show_Estudiantes():
    return showEstudiantes()

@app.get("/estudiante/{id}", response_model=EstudianteId)
async def show_one_estudiante(id:int):
    estudiante = showEstudiante(id)
    if not(estudiante):
        raise HTTPException(status_code=404, detail=f"{id} estudiante not found")
    return estudiante
