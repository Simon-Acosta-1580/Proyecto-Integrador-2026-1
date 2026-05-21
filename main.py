from fastapi import FastAPI, HTTPException
from operations.Estudiante_operations import createEstudiante, get_active_students,get_inactive_students, find_one_estudiante, find_one_estudiante_programa, update_one_student, delete_student, reactivate_estudiante
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
        raise HTTPException(status_code=409, detail=f"El estudiante con código {estudiante.codigo} ya existe.")
    return new_estudiante

@app.get("/estudiantes", response_model=list[EstudianteId], tags=["Estudiantes"])
async def read_estudiantes(session: SessionDep):
    lista_estudiantes = get_active_students(session)
    if not lista_estudiantes:
        raise HTTPException(status_code=409, detail=f"No se encontraron estudiantes registrados")
    return lista_estudiantes

@app.get("/estudiantesInactivos", response_model=list[EstudianteId], tags=["Estudiantes"])
async def show_estudiantesInactivos(session: SessionDep):
    estudiante_inactivos = get_inactive_students(session)
    if not estudiante_inactivos:
        raise HTTPException(status_code=404, detail="No estudiantes inactivos")
    return estudiante_inactivos

@app.get("/estudiante/buscar", response_model=EstudianteId, tags=["Estudiantes"])
async def show_estudiantes_programa(programa: str, session: SessionDep):
    estudiante = find_one_estudiante_programa(programa, session)
    if not estudiante:
        raise HTTPException(status_code=404, detail=f"No se encontro estudiante del programa: {programa}")
    return estudiante

@app.get("/estudiante/{id}", response_model=EstudianteId, tags=["Estudiantes"])
async def show_one_estudiante(id: int, session: SessionDep):
    estudiante = find_one_estudiante(id, session)
    if not estudiante:
        raise HTTPException(status_code=404,detail=f"No se encontro estudiante con id: {id}")
    return estudiante

@app.patch("/estudiante/{id}", response_model=EstudianteId, response_model_exclude={"id", "activo"}, tags=["Estudiantes"])
async def update_estudiante(id: int, estudiante: EstudianteUpdate, session: SessionDep):
    update = update_one_student(id, estudiante, session)
    if not (update):
        raise HTTPException(status_code=404, detail=f"{id} Estudiante not found")
    return update

@app.delete("/estudiante/{id}", response_model=EstudianteId, tags=["Estudiantes"])
async def delete_estudiante(id: int, session: SessionDep):
    estudiante_eliminado = delete_student(id, session)

    if not estudiante_eliminado:
        raise HTTPException(status_code=404, detail=f"Estudiante {id} no encontrado")

    return estudiante_eliminado

@app.patch("/estudiante/rehabilitar/{id}", response_model=EstudianteId, tags=["Estudiantes"])
def rehabilitar_estudiante(id: int, session: SessionDep):
    estudiante = reactivate_estudiante(id, session)

    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return estudiante

