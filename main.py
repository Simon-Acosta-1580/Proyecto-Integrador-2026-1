from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request, Depends
from starlette.responses import RedirectResponse

from operations.Estudiante_operations import createEstudiante, get_active_students,get_inactive_students, find_one_estudiante, find_one_estudiante_programa, update_one_student, delete_student, reactivate_estudiante
from operations.Implemento_operations import createImplemento, get_active_implements, get_inactive_implements, find_one_implement, find_one_implement_category, update_one_implement, delete_implement, reactivate_implement
from operations.turno_Operations import createTurno, get_active_turnos, get_inactive_turnos, find_one_turno, find_one_turno_horario, update_one_turno, delete_turno, reactivate_turno
from models import EstudianteBase, EstudianteId, EstudianteUpdate, ImplementoBase, ImplementoId,ImplementoUpdate, TurnoBase, TurnoId, TurnoUpdate
from sqlmodel import Session
from db import SessionDep, create_all_tables, get_session
from utils import save_img_local, save_img_remote
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(lifespan=create_all_tables)

templates = Jinja2Templates(directory="templates")

@app.post("/image/local")
async def image_save_local(img: UploadFile = File(...)):
    path = save_img_local(img)
    return {"path for your image": path}

@app.post("/image/remote")
async def image_save_remote(file:UploadFile = File(...)):
    url_img = save_img_remote(file)
    return {"url for your image":url_img}

@app.get("/hola", tags=["saludo"])
def hola():
    return {"message": "Hello World"}

@app.get("/", response_class=HTMLResponse)
async def templating(request: Request):
    return templates.TemplateResponse(
        request, "index.html"
    )

@app.get("/estudiante/nuevo", response_class=HTMLResponse, tags=["Vistas HTML"])
async def mostrar_formulario_estudiante(request: Request):
    return templates.TemplateResponse(
        request,
        name="crear_estudiante.html"
    )

@app.post("/estudiante/nuevo", response_class=HTMLResponse, tags=["Estudiantes"])
async def create_estudiante(
        codigo: int = Form(...),
        nombre: str = Form(...),
        programa: str = Form(...),
        file: Optional[UploadFile] = File(None),
        session: Session = Depends(get_session)
):
    url_supabase = None
    if file:
        url_supabase = await save_img_remote(file)

    estudiante_base = EstudianteBase(codigo=codigo, nombre=nombre, programa=programa)

    new_estudiante = createEstudiante(estudiante_base, session, imagen_url=url_supabase)

    if not new_estudiante:
        raise HTTPException(status_code=409, detail=f"El estudiante con código {codigo} ya existe.")

    return RedirectResponse(new_estudiante)


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


@app.patch("/estudiante/{id}", response_model=EstudianteId, response_model_exclude={"id", "activo"},
           tags=["Estudiantes"])
async def update_estudiante(
        id: int,
        nombre: Optional[str] = Form(None),
        programa: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        session: SessionDep = None
):
    estudiante_db = session.get(EstudianteId, id)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {id} no encontrado")

    url_supabase = None
    if file and file.filename:
        try:
            url_supabase = save_img_remote(file)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al subir la nueva imagen a Supabase: {str(e)}"
            )
    estudiante_update = EstudianteUpdate(
        nombre=nombre,
        programa=programa
    )
    updated_student = update_one_student(id, estudiante_update, session, imagen_url=url_supabase)

    return updated_student

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
async def create_implemento(
        codigo: int = Form(...),
        nombre: str = Form(...),
        categoria: str = Form(...),
        file: Optional[UploadFile] = File(None),
        session: SessionDep = None
):
    url_supabase = None
    if file:
        url_supabase = save_img_remote(file)

    implemento_base = ImplementoBase(codigo=codigo, nombre=nombre, categoria=categoria)

    new_implement = createImplemento(implemento_base, session, imagen_url=url_supabase)

    if not new_implement:
        raise HTTPException(status_code=409, detail=f"El implemento con código {codigo} ya existe.")

    return new_implement

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

@app.patch("/implemento/{id}", response_model=ImplementoId, response_model_exclude={"id", "activo"},
           tags=["Implementos"])
async def update_implemento(
        id: int,
        nombre: Optional[str] = Form(None),
        categoria: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        session: SessionDep = None
):
    implemento_db = session.get(ImplementoId, id)
    if not implemento_db:
        raise HTTPException(status_code=404, detail=f"Implemento con ID {id} no encontrado")

    url_supabase = None
    if file and file.filename:
        try:
            url_supabase = save_img_remote(file)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al subir la nueva imagen a Supabase: {str(e)}"
            )
    implemento_update = EstudianteUpdate(
        nombre=nombre,
        categoria=categoria
    )
    updated_implement = update_one_implement(id, implemento_update, session, imagen_url=url_supabase)

    return updated_implement

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

@app.post("/estudiante", response_model=EstudianteId, tags=["Estudiantes"])
async def create_estudiante(
        codigo: int = Form(...),
        nombre: str = Form(...),
        programa: str = Form(...),
        file: Optional[UploadFile] = File(None),
        session: SessionDep = None
):
    url_supabase = None
    if file:
        url_supabase = save_img_remote(file)

    estudiante_base = EstudianteBase(codigo=codigo, nombre=nombre, programa=programa)

    new_estudiante = createEstudiante(estudiante_base, session, imagen_url=url_supabase)

    if not new_estudiante:
        raise HTTPException(status_code=409, detail=f"El estudiante con código {codigo} ya existe.")

    return new_estudiante

@app.get("/", response_class=HTMLResponse)
async def templating(request: Request):
    return templates.TemplateResponse(
        request, "index.html"
    )

@app.get("/estudiante/nuevo", response_class=HTMLResponse, tags=["Vistas HTML"])
async def mostrar_formulario_estudiante(request: Request):
    return templates.TemplateResponse(
        request,
        name="crear_estudiante.html"
    )

@app.post("/estudiante/nuevo", response_class=HTMLResponse, tags=["Estudiantes"])
async def create_estudiante(
        codigo: int = Form(...),
        nombre: str = Form(...),
        programa: str = Form(...),
        file: Optional[UploadFile] = File(None),
        session: SessionDep = None
):
    url_supabase = None
    if file:
        url_supabase = save_img_remote(file)

    estudiante_base = EstudianteBase(codigo=codigo, nombre=nombre, programa=programa)

    new_estudiante = createEstudiante(estudiante_base, session, imagen_url=url_supabase)

    if not new_estudiante:
        raise HTTPException(status_code=409, detail=f"El estudiante con código {codigo} ya existe.")

    return new_estudiante
