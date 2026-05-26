from sqlmodel import Session, select
from models import TurnoBase, TurnoId, TurnoUpdate, EstudianteId, ImplementoId


def createTurno(turno: TurnoBase, session: Session):
    estudiante = session.get(EstudianteId, turno.estudiante_id)
    if not estudiante or not estudiante.activo:
        return None

    implemento = session.get(ImplementoId, turno.implemento_id)
    if not implemento or not implemento.activo:
        return None

    statement = select(TurnoId).where(TurnoId.codigo == turno.codigo)
    existing_turno = session.exec(statement).first()
    if existing_turno:
        return None

    new_turno = TurnoId.model_validate(turno)
    session.add(new_turno)

    estudiante.activo = False
    implemento.activo = False
    session.add(estudiante)
    session.add(implemento)

    session.commit()
    session.refresh(new_turno)
    return new_turno


def get_active_turnos(session: Session):
    statement = select(TurnoId).where(TurnoId.activo == True)
    return session.exec(statement).all()


def get_inactive_turnos(session: Session):
    statement = select(TurnoId).where(TurnoId.activo == False)
    return session.exec(statement).all()


def find_one_turno(id: int, session: Session):
    return session.get(TurnoId, id)


def find_one_turno_horario(horario: str, session: Session):
    statement = select(TurnoId).where(TurnoId.horario == horario)
    return session.exec(statement).first()


def update_one_turno(id: int, new_turno: TurnoUpdate, session: Session):
    turno_db = session.get(TurnoId, id)
    if not turno_db:
        return None

    estudiante_id_viejo = turno_db.estudiante_id
    implemento_id_viejo = turno_db.implemento_id

    try:
        update_data = new_turno.model_dump(exclude_unset=True)

        if "estudiante_id" in update_data and update_data["estudiante_id"] != estudiante_id_viejo:
            nuevo_estudiante = session.get(EstudianteId, update_data["estudiante_id"])
            if not nuevo_estudiante or not nuevo_estudiante.activo:
                return None

            nuevo_estudiante.activo = False
            session.add(nuevo_estudiante)

            estudiante_viejo = session.get(EstudianteId, estudiante_id_viejo)
            if estudiante_viejo:
                estudiante_viejo.activo = True
                session.add(estudiante_viejo)

        if "implemento_id" in update_data and update_data["implemento_id"] != implemento_id_viejo:
            nuevo_implemento = session.get(ImplementoId, update_data["implemento_id"])
            if not nuevo_implemento or not nuevo_implemento.activo:
                return None

            nuevo_implemento.activo = False
            session.add(nuevo_implemento)

            implemento_viejo = session.get(ImplementoId, implemento_id_viejo)
            if implemento_viejo:
                implemento_viejo.activo = True
                session.add(implemento_viejo)

        turno_db.sqlmodel_update(update_data)
        session.add(turno_db)

        session.commit()
        session.refresh(turno_db)
        return turno_db

    except Exception:
        session.rollback()
        return None


def delete_turno(id: int, session: Session):
    turno_db = session.get(TurnoId, id)
    if not turno_db:
        return None

    turno_db.activo = False
    session.add(turno_db)

    estudiante = session.get(EstudianteId, turno_db.estudiante_id)
    implemento = session.get(ImplementoId, turno_db.implemento_id)

    if estudiante:
        estudiante.activo = True
        session.add(estudiante)
    if implemento:
        implemento.activo = True
        session.add(implemento)

    session.commit()
    session.refresh(turno_db)
    return turno_db


def reactivate_turno(id: int, session: Session):
    turno_db = session.get(TurnoId, id)
    if not turno_db:
        return None

    estudiante = session.get(EstudianteId, turno_db.estudiante_id)
    implemento = session.get(ImplementoId, turno_db.implemento_id)

    if (estudiante and not estudiante.activo) or (implemento and not implemento.activo):
        return None

    turno_db.activo = True
    session.add(turno_db)

    if estudiante:
        estudiante.activo = False
        session.add(estudiante)
    if implemento:
        implemento.activo = False
        session.add(implemento)

    session.commit()
    session.refresh(turno_db)
    return turno_db