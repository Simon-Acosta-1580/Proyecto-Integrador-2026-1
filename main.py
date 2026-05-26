from fastapi import FastAPI, HTTPException
from operations.Estudiante_operations import createEstudiante, get_active_students,get_inactive_students, find_one_estudiante, find_one_estudiante_programa, update_one_student, delete_student, reactivate_estudiante
from operations.Implemento_operations import createImplemento, get_active_implements, get_inactive_implements, find_one_implement, find_one_implement_category, update_one_implement, delete_implement, reactivate_implement
from operations.turno_Operations import createTurno, get_active_turnos, get_inactive_turnos, find_one_turno, find_one_turno_horario, update_one_turno, delete_turno, reactivate_turno
from models import EstudianteBase, EstudianteId, EstudianteUpdate, ImplementoBase, ImplementoId,ImplementoUpdate, TurnoBase, TurnoId, TurnoUpdate
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
        raise HTTPException(status_code=404, detail="Estudiante no encontrado, verifique que estudiante no forme parte de un turno activo")

    return estudiante

@app.post("/implemento", response_model=ImplementoId, tags=["Implementos"])
async def create_implement(implemento: ImplementoBase, session: SessionDep):
    new_implemento=createImplemento(implemento, session)
    if not new_implemento:
        raise HTTPException(status_code=409, detail=f"El implemento con código {implemento.codigo} ya existe.")
    return new_implemento

@app.get("/implementos", response_model=list[ImplementoId], tags=["Implementos"])
async def read_implements(session: SessionDep):
    lista_implementos = get_active_implements(session)
    if not lista_implementos:
        raise HTTPException(status_code=404, detail=f"No se encontraron implementos registrados")
    return lista_implementos

@app.get("/implementosInactivos", response_model=list[ImplementoId], tags=["Implementos"])
async def show_implementosInactivos(session: SessionDep):
    implementos_inactivos = get_inactive_implements(session)
    if not implementos_inactivos:
        raise HTTPException(status_code=404, detail="No implementos inactivos")
    return implementos_inactivos

@app.get("/implemento/buscar", response_model=ImplementoId, tags=["Implementos"])
async def show_implementos_categoria(categoria: str, session: SessionDep):
    implemento = find_one_implement_category(categoria, session)
    if not implemento:
        raise HTTPException(status_code=404, detail=f"No se encontro implemento del categoria: {categoria}")
    return implemento

@app.get("/implemento/{id}", response_model=ImplementoId, tags=["Implementos"])
async def show_one_implement(id: int, session: SessionDep):
    implemento = find_one_implement(id, session)
    if not implemento:
        raise HTTPException(status_code=404,detail=f"No se encontro implemento con id: {id}")
    return implemento

@app.patch("/implemento/{id}", response_model=ImplementoId, response_model_exclude={"id", "activo"}, tags=["Implementos"])
async def update_implemento(id: int, implemento: ImplementoUpdate, session: SessionDep):
    updatei = update_one_implement(id, implemento, session)
    if not (updatei):
        raise HTTPException(status_code=404, detail=f"{id} Implemento not found")
    return updatei

@app.delete("/implemento/{id}", response_model=ImplementoId, tags=["Implementos"])
async def delete_implemento(id: int, session: SessionDep):
    implemento_eliminado = delete_implement(id, session)

    if not implemento_eliminado:
        raise HTTPException(status_code=404, detail=f"Implemento {id} no encontrado")

    return implemento_eliminado

@app.patch("/implemento/rehabilitar/{id}", response_model=ImplementoId, tags=["Implementos"])
def rehabilitar_implemento(id: int, session: SessionDep):
    implemento = reactivate_implement(id, session)

    if not implemento:
        raise HTTPException(status_code=404, detail="Implemento no encontrado, verifique que no forma parte de un turno activo")

    return implemento

@app.post("/turno", response_model=TurnoId, tags=["Turnos"])
async def create_turno(turno: TurnoBase, session: SessionDep):
    new_turno = createTurno(turno, session)
    if not new_turno:
        raise HTTPException(
            status_code=409,
            detail="No se pudo registrar el turno. Verifica que el estudiante y el implemento existan y estén activos, o que el código ya exista."
        )
    return new_turno


@app.get("/turnos", response_model=list[TurnoId], tags=["Turnos"])
async def read_turnos(session: SessionDep):
    lista_turnos = get_active_turnos(session)
    if not lista_turnos:
        raise HTTPException(status_code=404, detail="No se encontraron turnos registrados")
    return lista_turnos


@app.get("/turnosInactivos", response_model=list[TurnoId], tags=["Turnos"])
async def show_turnos_inactivos(session: SessionDep):
    turnos_inactivos = get_inactive_turnos(session)
    if not turnos_inactivos:
        raise HTTPException(status_code=404, detail="No hay turnos inactivos")
    return turnos_inactivos


@app.get("/turno/buscar", response_model=TurnoId, tags=["Turnos"])
async def show_turnos_horario(horario: str, session: SessionDep):
    turno = find_one_turno_horario(horario, session)
    if not turno:
        raise HTTPException(status_code=404, detail=f"No se encontró turno para el horario: {horario}")
    return turno


@app.get("/turno/{id}", response_model=TurnoId, tags=["Turnos"])
async def show_one_turno(id: int, session: SessionDep):
    turno = find_one_turno(id, session)
    if not turno:
        raise HTTPException(status_code=404, detail=f"No se encontró turno con id: {id}")
    return turno


@app.patch("/turno/{id}", response_model=TurnoId, response_model_exclude={"id", "activo"}, tags=["Turnos"])
async def update_turno(id: int, turno: TurnoUpdate, session: SessionDep):
    updatet = update_one_turno(id, turno, session)
    if not updatet:
        raise HTTPException(status_code=404, detail=f"Turno {id} not found")
    return updatet


@app.delete("/turno/{id}", response_model=TurnoId, tags=["Turnos"])
async def delete_turno_endpoint(id: int, session: SessionDep):
    turno_eliminado = delete_turno(id, session)
    if not turno_eliminado:
        raise HTTPException(status_code=404, detail=f"Turno {id} no encontrado")
    return turno_eliminado


@app.patch("/turno/rehabilitar/{id}", response_model=TurnoId, tags=["Turnos"])
async def rehabilitar_turno(id: int, session: SessionDep):
    turno = reactivate_turno(id, session)
    if not turno:
        raise HTTPException(
            status_code=400,
            detail="No se pudo rehabilitar el turno. Puede que no exista o que el estudiante/implemento ya estén asignados."
        )
    return turno
