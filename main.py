from fastapi import FastAPI, HTTPException
from Estudiante_operations import createEstudiante, showEstudiantes, showEstudiante, deleteEstudiante, updateEstudiante
from Implemento_operations import createImplemento, showImplementos, showImplemento, deleteImplemento, updateImplemento
from models import EstudianteBase, EstudianteId, ImplementoBase, ImplementoId

app = FastAPI()

@app.get("/hola")
def hola():
    return {"message": "Hello World"}

@app.post("/estudiante", response_model=EstudianteId)
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

@app.get("/estudiante/{id}", response_model=EstudianteId)
async def show_one_estudiante(id:int):
    estudiante = showEstudiante(id)
    if not(estudiante):
        raise HTTPException(status_code=404, detail=f"{id} estudiante not found")
    return estudiante

@app.delete("/estudiante/{id}", response_model=EstudianteBase)
async def delete_one_estudiante(id:int):
    deleted = deleteEstudiante(id)
    if not(deleted):
        raise HTTPException(status_code=404, detail=f"{id} Estudiante not found")
    return deleted

@app.patch("/estudiante/{id}", response_model=EstudianteId)
async def edit_estudiante(id: int, datos_nuevos: EstudianteBase):
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

@app.get("/implemento/{id}", response_model=ImplementoId)
async def show_one_implemento(id:int):
    implemento = showImplemento(id)
    if not(implemento):
        raise HTTPException(status_code=404, detail=f"{id} implemento not found")
    return implemento

@app.delete("/implemento/{id}", response_model=ImplementoBase)
async def delete_one_implemento(id:int):
    deleted = deleteImplemento(id)
    if not(deleted):
        raise HTTPException(status_code=404, detail=f"{id} Implemento not found")
    return deleted

@app.patch("/implemento/{id}", response_model=ImplementoId)
async def edit_implemento(id: int, datos_nuevos: ImplementoBase):
    implemento_editado = updateImplemento(id, datos_nuevos)
    if not implemento_editado:
        raise HTTPException(status_code=404, detail=f"Implemento con ID {id} no encontrado")
    return implemento_editado


