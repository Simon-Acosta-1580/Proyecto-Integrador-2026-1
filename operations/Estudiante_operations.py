from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import EstudianteBase, EstudianteId, EstudianteUpdate, TurnoId


def createEstudiante(estudiante: EstudianteBase, session: Session):
    statement = select(EstudianteId).where(EstudianteId.codigo == estudiante.codigo)
    existing_estudiante = session.exec(statement).first()

    if existing_estudiante:
        return None

    new_estudiante = EstudianteId.model_validate(estudiante)
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

def update_one_student(id: int, new_estudiante: EstudianteUpdate, session: Session):
    estudiante_db = session.get(EstudianteId, id)

    if not estudiante_db:
        return None

    try:
        update_data = new_estudiante.model_dump(exclude_unset=True)

        estudiante_db.sqlmodel_update(update_data)

        session.add(estudiante_db)
        session.commit()
        session.refresh(estudiante_db)
        return estudiante_db

    except Exception as e:
        return None

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
