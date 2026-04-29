from fastapi import FastAPI, HTTPException
from Estudiante_operations import createEstudiante, showEstudiantes, showEstudiantesInactivos, showEstudiante, getEstudianteByPrograma, deleteEstudiante, updateEstudiante
from Implemento_operations import createImplemento, showImplementos, showImplementosInactivos, showImplemento, getImplementoByCategoria, deleteImplemento, updateImplemento
from turno_Operations import createTurno, showTurnos, showTurno, showTurnosInactivos, getTurnosByHorario, deleteTurno, updateTurno
from models import EstudianteBase, EstudianteId, ImplementoBase, ImplementoId, TurnoBase, TurnoId

app = FastAPI()

@app.get("/hola")
def hola():
    return {"message": "Hello World"}

@app.post("/estudiante", response_model=EstudianteBase)
async def create_estudiante(estudiante:EstudianteBase):
    return createEstudiante(estudiante)

@app.get("/estudiantes/", response_model=list[EstudianteId])
async def show_all_estudiantes():
    lista_estudiantes = showEstudiantes()

    if not lista_estudiantes:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron estudiantes registrados."
        )

    return lista_estudiantes

@app.get("/estudiantesInactivos/", response_model=list[EstudianteId])
async def show_all_estudiantes_inactivos():
    lista_estudiantes = showEstudiantesInactivos()
    if not lista_estudiantes:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron estudiantes inactivos registrados."
        )
    return lista_estudiantes

@app.get("/estudiante/{id}", response_model=EstudianteId)
async def show_one_estudiante(id:int):
    estudiante = showEstudiante(id)
    if not(estudiante):
        raise HTTPException(status_code=404, detail=f"{id} estudiante not found")
    return estudiante

@app.get("/estudiante/buscar/", response_model=list[EstudianteId])
async def buscar_por_programa(programa: str):
    resultados = getEstudianteByPrograma(programa)

    if resultados is None:
        raise HTTPException(
            status_code=400,
            detail="Categoria no valida, unicamente 'ingenieria', 'derecho', 'arquitectura', 'psicologia'."
        )

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron estudiantes activos en el programa: {programa}"
        )

    return resultados

@app.delete("/estudiante/{id}", response_model=EstudianteBase)
async def delete_one_estudiante(id: int):
    deleted = deleteEstudiante(id)

    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {id} no encontrado")

    return deleted

@app.patch("/estudiante/{id}", response_model=EstudianteId)
async def update_estudiante(id: int, datos_nuevos: EstudianteBase):
    estudiante_editado = updateEstudiante(id, datos_nuevos)
    if not estudiante_editado:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {id} no encontrado")
    return estudiante_editado

@app.post("/implemento", response_model=ImplementoBase)
async def create_implemento(implemento:ImplementoBase):
    return createImplemento(implemento)

@app.get("/implementos/", response_model=list[ImplementoId])
async def show_all_implementos():
    lista_implementos = showImplementos()

    if not lista_implementos:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron implementos registrados."
        )

    return lista_implementos

@app.get("/implementosInactivos/", response_model=list[ImplementoId])
async def show_all_implementos_inactivos():
    lista_implementos = showImplementosInactivos()
    if not lista_implementos:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron implementos inactivos registrados."
        )
    return lista_implementos

@app.get("/implemento/{id}", response_model=ImplementoId)
async def show_one_implemento(id:int):
    implemento = showImplemento(id)
    if not(implemento):
        raise HTTPException(status_code=404, detail=f"{id} implemento not found")
    return implemento

@app.get("/implemento/buscar/", response_model=list[ImplementoId])
async def buscar_por_categoria(categoria: str):
    resultados = getImplementoByCategoria(categoria)

    if resultados is None:
        raise HTTPException(
            status_code=400,
            detail="Categoria no valida, unicamente 'balon', 'instrumento', 'juego', 'cancha'."
        )

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron implementos activos en la categoria: {categoria}"
        )

    return resultados

@app.delete("/implemento/{id}", response_model=ImplementoBase)
async def delete_one_implemento(id: int):
    deleted = deleteImplemento(id)

    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Implemento con ID {id} no encontrado")

    return deleted

@app.patch("/implemento/{id}", response_model=ImplementoId)
async def update_implemento(id: int, datos_nuevos: ImplementoBase):
    implemento_editado = updateImplemento(id, datos_nuevos)
    if not implemento_editado:
        raise HTTPException(status_code=404, detail=f"Implemento con ID {id} no encontrado")
    return implemento_editado

@app.post("/turno", response_model=TurnoId)
async def create_turno(turno: TurnoBase):
    return createTurno(turno)

@app.get("/turnos/", response_model=list[TurnoId])
async def show_all_turnos():
    lista_turnos = showTurnos()

    if not lista_turnos:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron turnos registrados."
        )

    return lista_turnos

@app.get("/turnosInactivos/", response_model=list[TurnoId])
async def show_all_turnos_inactivos():
    lista_turnos = showTurnosInactivos()
    if not lista_turnos:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron turnos inactivos registrados."
        )
    return lista_turnos

@app.get("/turno/{id}", response_model=TurnoId)
async def show_one_turno(id:int):
    turno = showTurno(id)
    if not(turno):
        raise HTTPException(status_code=404, detail=f"{id} turno not found")
    return turno


@app.get("/turnos/buscar/", response_model=list[TurnoId])
async def buscar_por_horario(horario: str):
    resultados = getTurnosByHorario(horario)

    if resultados is None:
        raise HTTPException(
            status_code=400,
            detail="Horario no válido. Debe ser 'diurno' o 'nocturno'."
        )

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron turnos activos en el horario: {horario}"
        )

    return resultados

@app.delete("/turno/{id}", response_model=TurnoBase)
async def delete_one_turno(id: int):
    deleted = deleteTurno(id)

    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Turno con ID {id} no encontrado")

    return deleted

@app.patch("/turno/{id}", response_model=TurnoId)
async def update_turno(id: int, datos_nuevos: TurnoBase):
    turno_editado = updateTurno(id, datos_nuevos)
    if not turno_editado:
        raise HTTPException(status_code=404, detail=f"Turno con ID {id} no encontrado")
    return turno_editado


