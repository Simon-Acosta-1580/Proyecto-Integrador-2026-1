import os
import csv
from models import EstudianteBase, EstudianteId
from fastapi import HTTPException
from typing import Optional

CSV_FILE = "estudiante.csv"
columns = ["id", "nombre", "programa", "codigo", "activo"]

def newID():
    if not os.path.exists(CSV_FILE):
        return 1
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            ids = [int(row["id"]) for row in reader]
            return max(ids) + 1 if ids else 1
    except (FileNotFoundError, csv.Error, ValueError):
        return 1

def saveEstudianteID(estudiante: EstudianteId):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        writer.writerow(estudiante.model_dump())

def createEstudiante(estudiante: EstudianteId):
    existing_estudiantes = getAllEstudiantes()

    for e in existing_estudiantes:
        if e.activo == True and e.codigo == estudiante.codigo:
            raise HTTPException(status_code=400, detail=f"El estudiante con código {estudiante.codigo} ya existe.")

    id = newID()
    new_estudiante = EstudianteId(id=id, **estudiante.model_dump(exclude={'id'}))
    saveEstudianteID(new_estudiante)
    return new_estudiante

def getAllEstudiantes():
    if not os.path.exists(CSV_FILE):
        return []
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            return [EstudianteId(**row) for row in reader]
    except (FileNotFoundError, csv.Error):
        return []

def showEstudiantes():
    all_estudiantes = getAllEstudiantes()
    return [estudiante for estudiante in all_estudiantes if estudiante.activo is True or str(estudiante.activo).lower() == 'true']

def showEstudiantesInactivos():
    all_estudiantes = getAllEstudiantes()
    return [estudiante for estudiante in all_estudiantes if estudiante.activo is False or str(estudiante.activo).lower() == 'false']

def showEstudiante(id:int):
    with open(CSV_FILE) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["id"]) == id:
                return EstudianteId(**row)

def getEstudianteByPrograma(tipo_programa: str):
    tipo_programa = tipo_programa.lower()

    if tipo_programa not in ["ingenieria", "derecho", "arquitectura", "psicologia"]:
        return None

    all_estudiantes = getAllEstudiantes()
    busqueda = [e for e in all_estudiantes if e.programa.lower() == tipo_programa and e.activo]

    return busqueda

def deleteEstudiante(id: int):
    estudiante_deleted: Optional[EstudianteId] = None
    estudiantes = getAllEstudiantes()

    with open(CSV_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for estudiante in estudiantes:
            if int(estudiante.id) == id:
                estudiante.activo = False
                estudiante_deleted = estudiante

            writer.writerow(estudiante.model_dump())

    return estudiante_deleted

def updateEstudiante(id: int, estudiante_actualizado: EstudianteBase) -> Optional[EstudianteId]:
    estudiantes = getAllEstudiantes()
    encontrado = False
    lista_actualizada = []
    resultado = None

    for estudiante_existente in estudiantes:
        if int(estudiante_existente.id) == id:
            datos_nuevos = estudiante_actualizado.model_dump(exclude={'id', 'codigo', 'activo'})

            nuevo_estudiante = EstudianteId(
                id=id,
                codigo=estudiante_existente.codigo,
                activo=estudiante_existente.activo,
                **datos_nuevos
            )

            lista_actualizada.append(nuevo_estudiante)
            resultado = nuevo_estudiante
            encontrado = True
        else:
            lista_actualizada.append(estudiante_existente)

    if encontrado:
        with open(CSV_FILE, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for e in lista_actualizada:
                writer.writerow(e.model_dump())
        return resultado

    return None

