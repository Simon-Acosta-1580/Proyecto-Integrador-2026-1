from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import EstudianteBase, EstudianteId, EstudianteUpdate, TurnoId
from typing import Optional


def createEstudiante(estudiante_data: EstudianteBase, session: Session, imagen_url: Optional[str] = None):
    statement = select(EstudianteId).where(EstudianteId.codigo == estudiante_data.codigo)
    db_estudiante = session.exec(statement).first()
    if db_estudiante:
        return None

    new_estudiante = EstudianteId(
        codigo=estudiante_data.codigo,
        nombre=estudiante_data.nombre,
        programa=estudiante_data.programa,
        imagen=imagen_url
    )

    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)
    return new_estudiante


def get_active_students(session: Session):
    statement = select(EstudianteId).where(EstudianteId.activo == True)
    results = session.exec(statement).all()
    return results

def get_inactive_students(session: Session):
    statement = select(EstudianteId).where(EstudianteId.activo == False)
    results = session.exec(statement).all()
    return results

def find_one_estudiante(id: int, session: Session):
    try:
        return session.get(EstudianteId, id)
    except NoResultFound:
        return None

def find_one_estudiante_programa(programa: str, session: Session):
    try:
        statement = select(EstudianteId).where(EstudianteId.programa == programa)
        result = session.exec(statement).first()
        return result
    except Exception:
        return None


def update_one_student(id: int, estudiante_data: EstudianteUpdate, session: Session, imagen_url: Optional[str] = None):
    estudiante_db = session.get(EstudianteId, id)
    if not estudiante_db:
        return None

    data_dict = estudiante_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(estudiante_db, key, value)

    if imagen_url:
        estudiante_db.imagen = imagen_url

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)
    return estudiante_db

def delete_student(id: int, session: Session):
    estudiante_db = session.get(EstudianteId, id)

    if not estudiante_db:
        return None

    estudiante_db.activo = False

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)

    return estudiante_db

def reactivate_estudiante(id: int, session: Session):
    estudiante_db = session.get(EstudianteId, id)

    if not estudiante_db:
        return None

    statement = select(TurnoId).where(
        TurnoId.implemento_id == id,
        TurnoId.activo == True
    )
    turno_activo_con_estudiante = session.exec(statement).first()

    if turno_activo_con_estudiante:
        return None

    estudiante_db.activo = True

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)

    return estudiante_db
