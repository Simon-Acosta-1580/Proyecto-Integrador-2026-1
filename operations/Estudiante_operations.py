from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import EstudianteBase, EstudianteId

def createEstudiante(estudiante: EstudianteBase, session: Session):
    new_estudiante = EstudianteId.model_validate(estudiante)
    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)

    return new_estudiante
