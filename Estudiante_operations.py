import os
import csv
from models import EstudianteBase, EstudianteId
from typing import Optional

CSV_FILE = "estudiante.csv"
columns = ["id", "nombre", "programa", "codigo"]

def newID():
    try:
        with open(CSV_FILE, mode="r",newline='') as file:
            reader = csv.DictReader(file)
            max_id = max(int(row["id"]) for row in reader)
            return max_id+1
    except (FileNotFoundError, csv.Error):
        return 1

def saveEstudianteID(pokemon:EstudianteId):
    estudiante_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a+",newline='') as file:
        writer = csv.DictWriter(file,fieldnames=columns)
        if not estudiante_exists:
            writer.writeheader()
        writer.writerow(pokemon.model_dump())

def createEstudiante(pokemon:EstudianteBase):
    id = newID()
    new_pokemon = EstudianteId(id=id,**pokemon.model_dump())
    saveEstudianteID(new_pokemon)
    return new_pokemon

def showEstudiantes():
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            return [EstudianteId(**row) for row in reader]
    except FileNotFoundError:
        return []

def showEstudiante(id:int):
    with open(CSV_FILE) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["id"]) == id:
                return EstudianteId(**row)

def deleteEstudiante(id:int):
    estudiante_deleted: Optional[EstudianteBase]=None
    estudiantes = showEstudiantes()
    with open(CSV_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        for estudiante_ in estudiantes:
            if estudiante_.id == id:
                estudiante_deleted = estudiante_
                continue
            writer.writerow(estudiante_.model_dump())
    if estudiante_deleted:
        dict_estudiante_no_id = estudiante_deleted.model_dump()
        del dict_estudiante_no_id["id"]
        return EstudianteBase(**dict_estudiante_no_id)


def updateEstudiante(id: int, estudiante_actualizado: EstudianteBase) -> Optional[EstudianteId]:
    estudiantes = showEstudiantes()
    encontrado = False
    lista_actualizada = []
    resultado = None

    for est in estudiantes:
        if est.id == id:
            nuevo_estudiante = EstudianteId(id=id, **estudiante_actualizado.model_dump())
            lista_actualizada.append(nuevo_estudiante)
            resultado = nuevo_estudiante
            encontrado = True
        else:
            lista_actualizada.append(est)

    if encontrado:
        with open(CSV_FILE, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for e in lista_actualizada:
                writer.writerow(e.model_dump())
        return resultado

    return None
