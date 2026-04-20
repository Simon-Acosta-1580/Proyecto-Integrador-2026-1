from typing import List
from fastapi import FastAPI, HTTPException
from Estudiante_operations import createEstudiante
from models import (EstudianteBase, EstudianteId)

app = FastAPI()

@app.get("/hola")
def hola():
    return {"message": "Hello World"}

@app.post("/pokemon", response_model=EstudianteId)
async def create_pokemon(pokemon:EstudianteBase):
    return createEstudiante(pokemon)