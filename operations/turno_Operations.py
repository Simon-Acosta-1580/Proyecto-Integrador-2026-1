from typing import Optional, List
from sqlmodel import Session, select
from models import TurnoId, TurnoBase, TurnoCreate, TurnoUpdate, EstudianteId, ImplementoId


def createTurno(turno: TurnoCreate, session: Session) -> Optional[TurnoId]:
    try:
        # 1. Validar existencia y disponibilidad del estudiante
        estudiante = session.get(EstudianteId, turno.estudiante_id)
        if not estudiante or not estudiante.activo:
            return None

        # 2. Validar existencia y disponibilidad del implemento
        implemento = session.get(ImplementoId, turno.implemento_id)
        if not implemento or not implemento.activo:
            return None

        # 3. Evitar códigos de préstamo duplicados
        statement = select(TurnoId).where(TurnoId.codigo == turno.codigo)
        existing_turno = session.exec(statement).first()
        if existing_turno:
            return None

        # 4. Crear la instancia del Turno (mapea automáticamente los campos base)
        new_turno = TurnoId.model_validate(turno)
        session.add(new_turno)

        # 5. Lógica de negocio institucional: Ocupar recursos
        estudiante.activo = False
        implemento.activo = False
        session.add(estudiante)
        session.add(implemento)

        # 6. Consolidar cambios de forma segura
        session.commit()
        session.refresh(new_turno)
        return new_turno

    except Exception as e:
        session.rollback()
        print(f"Error al crear el turno en la base de datos: {e}")
        return None


def get_active_turnos(session: Session) -> List[TurnoId]:
    statement = select(TurnoId).where(TurnoId.activo == True)
    return session.exec(statement).all()


def get_inactive_turnos(session: Session) -> List[TurnoId]:
    statement = select(TurnoId).where(TurnoId.activo == False)
    return session.exec(statement).all()


def find_one_turno(id: int, session: Session) -> Optional[TurnoId]:
    return session.get(TurnoId, id)


def update_one_turno(id: int, new_turno: TurnoUpdate, session: Session) -> Optional[TurnoId]:
    turno_db = session.get(TurnoId, id)
    if not turno_db:
        return None

    estudiante_id_viejo = turno_db.estudiante_id
    implemento_id_viejo = turno_db.implemento_id

    try:
        # Extraemos los campos que vienen del formulario (estudiante_id e implemento_id)
        update_data = new_turno.model_dump(exclude_unset=True)

        # Intercambio dinámico de Estudiante si cambió en el selector HTML
        if "estudiante_id" in update_data and update_data["estudiante_id"] != estudiante_id_viejo:
            nuevo_estudiante = session.get(EstudianteId, update_data["estudiante_id"])
            if not nuevo_estudiante or not nuevo_estudiante.activo:
                return None  # No se puede asignar a un estudiante ocupado o inexistente

            nuevo_estudiante.activo = False
            session.add(nuevo_estudiante)

            # Liberamos al estudiante anterior
            estudiante_viejo = session.get(EstudianteId, estudiante_id_viejo)
            if estudiante_viejo:
                estudiante_viejo.activo = True
                session.add(estudiante_viejo)

        # Intercambio dinámico de Implemento si cambió en el selector HTML
        if "implemento_id" in update_data and update_data["implemento_id"] != implemento_id_viejo:
            nuevo_implemento = session.get(ImplementoId, update_data["implemento_id"])
            if not nuevo_implemento or not nuevo_implemento.activo:
                return None  # No se puede prestar un implemento ocupado o inexistente

            nuevo_implemento.activo = False
            session.add(nuevo_implemento)

            # Liberamos el implemento anterior
            implemento_viejo = session.get(ImplementoId, implemento_id_viejo)
            if implemento_viejo:
                implemento_viejo.activo = True
                session.add(implemento_viejo)

        # Mapeo y actualización segura de las propiedades en memoria
        for key, value in update_data.items():
            setattr(turno_db, key, value)

        session.add(turno_db)
        session.commit()
        session.refresh(turno_db)
        return turno_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar el turno: {e}")
        return None


def delete_turno(id: int, session: Session) -> Optional[TurnoId]:
    turno_db = session.get(TurnoId, id)
    if not turno_db:
        return None

    try:
        # Al finalizar o cancelar el turno, marcamos como inactivo el préstamo
        turno_db.activo = False
        session.add(turno_db)

        # Liberamos los recursos institucionales vinculados para que vuelvan a estar disponibles
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

    except Exception as e:
        session.rollback()
        print(f"Error al finalizar el turno: {e}")
        return None


def reactivate_turno(id: int, session: Session) -> Optional[TurnoId]:
    turno_db = session.get(TurnoId, id)
    if not turno_db:
        return None

    try:
        estudiante = session.get(EstudianteId, turno_db.estudiante_id)
        implemento = session.get(ImplementoId, turno_db.implemento_id)

        # Si el estudiante o el implemento original están ocupados en otro servicio activo, frena la reactivación
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

    except Exception as e:
        session.rollback()
        print(f"Error al reactivar el turno: {e}")
        return None