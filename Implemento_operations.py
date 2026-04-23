import os
import csv
from models import ImplementoBase, ImplementoId
from typing import Optional

CSV_FILE = "implemento.csv"
columns = ["id", "nombre", "categoria"]

def newID():
    try:
        with open(CSV_FILE, mode="r",newline='') as file:
            reader = csv.DictReader(file)
            max_id = max(int(row["id"]) for row in reader)
            return max_id+1
    except (FileNotFoundError, csv.Error):
        return 1

def saveImplementoID(implemento:ImplementoBase):
    implemento_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a+",newline='') as file:
        writer = csv.DictWriter(file,fieldnames=columns)
        if not implemento_exists:
            writer.writeheader()
        writer.writerow(implemento.model_dump())

def createImplemento(implemento:ImplementoBase):
    id = newID()
    new_implemento = ImplementoId(id=id,**implemento.model_dump())
    saveImplementoID(new_implemento)
    return new_implemento

def showImplementos():
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            return [ImplementoId(**row) for row in reader]
    except FileNotFoundError:
        return []

def showImplemento(id:int):
    with open(CSV_FILE) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["id"]) == id:
                return ImplementoId(**row)

def deleteImplemento(id:int):
    implemento_deleted: Optional[ImplementoBase]=None
    implementos = showImplementos()
    with open(CSV_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        for implemento_ in implementos:
            if implemento_.id == id:
                implemento_deleted = implemento_
                continue
            writer.writerow(implemento_.model_dump())
    if implemento_deleted:
        dict_implemento_no_id = implemento_deleted.model_dump()
        del dict_implemento_no_id["id"]
        return ImplementoBase(**dict_implemento_no_id)

def updateImplemento(id: int, implemento_actualizado: ImplementoBase) -> Optional[ImplementoId]:
    implementos = showImplementos()
    encontrado = False
    lista_actualizada = []
    resultado = None

    for est in implementos:
        if est.id == id:
            nuevo_implemento = ImplementoId(id=id, **implemento_actualizado.model_dump())
            lista_actualizada.append(nuevo_implemento)
            resultado = nuevo_implemento
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

