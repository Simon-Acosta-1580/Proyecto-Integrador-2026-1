from fastapi import FastAPI, HTTPException
from operations.Estudiante_operations import createEstudiante, show_all_estudiantes, find_one_estudiante
from operations.Implemento_operations import createImplemento, showImplementos, showImplementosInactivos, showImplemento, getImplementoByCategoria, deleteImplemento, updateImplemento
from operations.turno_Operations import createTurno, showTurnos, showTurno, showTurnosInactivos, getTurnosByHorario, deleteTurno, updateTurno
from models import EstudianteBase, EstudianteId, EstudianteUpdate, ImplementoBase, ImplementoId, TurnoBase, TurnoId
from sqlmodel import Session
from db import SessionDep, create_all_tables

app = FastAPI(lifespan=create_all_tables)

@app.get("/hola", tags=["saludo"])
def hola():
    return {"message": "Hello World"}

@app.post("/estudiante", response_model=EstudianteId, tags=["Estudiantes"])
async def create_estudiante(estudiante: EstudianteBase, session: SessionDep):
    new_estudiante=createEstudiante(estudiante, session)
    if not new_estudiante:
        raise HTTPException(status_code=404, detail=f"El estudiante con código {estudiante.codigo} ya existe.")

@app.get("/estudiantes", response_model=list[EstudianteId], tags=["Estudiantes"])
async def read_estudiantes(session: SessionDep):
    lista_estudiantes = show_all_estudiantes(session)
    if not lista_estudiantes:
        raise HTTPException(status_code=404, detail=f"No se encontraron estudiantes registrados")
    return lista_estudiantes

@app.get("/estudiante/{id}", response_model=EstudianteId, tags=["Estudiantes"])
async def show_one_estudiante(id: int, session: SessionDep):
    estudiante = find_one_estudiante(id, session)
    if not estudiante:
        raise HTTPException(status_code=404,detail=f"No se encontro estudiante con id: {id}")
    return estudiante


