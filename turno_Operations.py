import os
import csv
from models import TurnoBase, TurnoId
from fastapi import HTTPException
from typing import Optional

CSV_FILE = "Turno.csv"
columns = ["id", "codigo", "hora_inicio", "horario", "activo"]

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

def saveTurnoID(turno: TurnoId):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        writer.writerow(turno.model_dump())

def createTurno(turno: TurnoBase):
    existing_turnos = getAllTurnos()

    for t in existing_turnos:
        if t.activo == True and t.codigo == turno.codigo:
            raise HTTPException(status_code=400, detail=f"El turno con código {turno.codigo} ya existe.")

    id = newID()
    new_turno = TurnoId(id=id, **turno.model_dump(exclude={'id'}))
    saveTurnoID(new_turno)
    return new_turno
def getAllTurnos():
    if not os.path.exists(CSV_FILE):
        return []
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            return [TurnoId(**row) for row in reader]
    except (FileNotFoundError, csv.Error):
        return []

def showTurnos():
    all_turnos = getAllTurnos()
    return [turno for turno in all_turnos if turno.activo is True or str(turno.activo).lower() == 'true']

def showTurnosInactivos():
    all_turnos = getAllTurnos()
    return [turno for turno in all_turnos if turno.activo is False or str(turno.activo).lower() == 'false']

def showTurno(id:int):
    with open(CSV_FILE) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["id"]) == id:
                return TurnoId(**row)


def getTurnosByHorario(tipo_horario: str):
    tipo_horario = tipo_horario.lower()

    if tipo_horario not in ["diurno", "nocturno"]:
        return None

    all_turnos = getAllTurnos()
    busqueda = [t for t in all_turnos if t.horario.lower() == tipo_horario and t.activo]

    return busqueda

def deleteTurno(id: int):
    turno_deleted: Optional[TurnoId] = None
    turnos = getAllTurnos()

    with open(CSV_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for turno in turnos:
            if int(turno.id) == id:
                turno.activo = False
                turno_deleted = turno

            writer.writerow(turno.model_dump())

    return turno_deleted

def updateTurno(id: int, turno_actualizado: TurnoBase) -> Optional[TurnoId]:
    turnos = getAllTurnos()
    encontrado = False
    lista_actualizada = []
    resultado = None

    for turno_existente in turnos:
        if int(turno_existente.id) == id:
            datos_nuevos = turno_actualizado.model_dump(exclude={'id', 'codigo', 'activo'})

            nuevo_turno = TurnoId(
                id=id,
                codigo=turno_existente.codigo,
                activo=turno_existente.activo,
                **datos_nuevos
            )

            lista_actualizada.append(nuevo_turno)
            resultado = nuevo_turno
            encontrado = True
        else:
            lista_actualizada.append(turno_existente)

    if encontrado:
        with open(CSV_FILE, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for e in lista_actualizada:
                writer.writerow(e.model_dump())
        return resultado

    return None