from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import EstudianteBase, EstudianteId

def createEstudiante(estudiante: EstudianteBase, session: Session):
    lista_estudiantes = show_all_estudiantes(session)
    for e in lista_estudiantes:
        if e.codigo == estudiante.codigo:
            return None
    new_estudiante = EstudianteId.model_validate(estudiante)
    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)

    return new_estudiante

def show_all_estudiantes(session: Session):
    return session.exec(select(EstudianteId))
