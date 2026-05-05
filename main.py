from fastapi import FastAPI, HTTPException
from operations.Estudiante_operations import createEstudiante
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
    return createEstudiante(estudiante, session)




