import os
import csv
from models import EstudianteBase, EstudianteId

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