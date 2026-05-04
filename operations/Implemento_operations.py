import os
import csv
from fastapi import HTTPException
from models import ImplementoBase, ImplementoId
from typing import Optional

CSV_FILE = "implemento.csv"
columns = ["id", "nombre", "codigo", "categoria", "activo"]

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

def saveImplementoID(implemento: ImplementoId):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        writer.writerow(implemento.model_dump())

def createImplemento(implemento: ImplementoId):
    existing_implementos = getAllImplementos()

    for i in existing_implementos:
        if i.activo == True and i.codigo == implemento.codigo:
            raise HTTPException(status_code=400, detail=f"El implemento con código {implemento.codigo} ya existe.")

    id = newID()
    new_implemento = ImplementoId(id=id, **implemento.model_dump(exclude={'id'}))
    saveImplementoID(new_implemento)
    return new_implemento

def getAllImplementos():
    if not os.path.exists(CSV_FILE):
        return []
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            return [ImplementoId(**row) for row in reader]
    except (FileNotFoundError, csv.Error):
        return []

def showImplementos():
    all_implementos = getAllImplementos()
    return [implemento for implemento in all_implementos if implemento.activo is True or str(implemento.activo).lower() == 'true']

def showImplementosInactivos():
    all_implementos = getAllImplementos()
    return [implemento for implemento in all_implementos if implemento.activo is False or str(implemento.activo).lower() == 'false']

def showImplemento(id:int):
    with open(CSV_FILE) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["id"]) == id:
                return ImplementoId(**row)

def getImplementoByCategoria(tipo_categoria: str):
    tipo_categoria = tipo_categoria.lower()

    if tipo_categoria not in ["balon", "instrumento", "juego", "cancha"]:
        return None

    all_implementos = getAllImplementos()
    busqueda = [i for i in all_implementos if i.categoria.lower() == tipo_categoria and i.activo]

    return busqueda

def deleteImplemento(id: int):
    implemento_deleted: Optional[ImplementoId] = None
    implementos = getAllImplementos()

    with open(CSV_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for implemento in implementos:
            if int(implemento.id) == id:
                implemento.activo = False
                implemento_deleted = implemento

            writer.writerow(implemento.model_dump())

    return implemento_deleted

def updateImplemento(id: int, implemento_actualizado: ImplementoBase) -> Optional[ImplementoId]:
    implementos = getAllImplementos()
    encontrado = False
    lista_actualizada = []
    resultado = None

    for implemento_existente in implementos:
        if int(implemento_existente.id) == id:
            datos_nuevos = implemento_actualizado.model_dump(exclude={'id', 'codigo', 'activo'})

            nuevo_implemento = ImplementoId(
                id=id,
                codigo=implemento_existente.codigo,
                activo=implemento_existente.activo,
                **datos_nuevos
            )

            lista_actualizada.append(nuevo_implemento)
            resultado = nuevo_implemento
            encontrado = True
        else:
            lista_actualizada.append(implemento_existente)

    if encontrado:
        with open(CSV_FILE, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for e in lista_actualizada:
                writer.writerow(e.model_dump())
        return resultado

    return None

