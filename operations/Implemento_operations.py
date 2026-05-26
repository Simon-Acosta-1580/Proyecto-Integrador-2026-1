from models import ImplementoBase, ImplementoId, ImplementoUpdate, TurnoId
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

def createImplemento(implemento: ImplementoBase, session: Session):
    statement = select(ImplementoId).where(ImplementoId.codigo == implemento.codigo)
    existing_implemento = session.exec(statement).first()

    if existing_implemento:
        return None

    new_implemento = ImplementoId.model_validate(implemento)
    session.add(new_implemento)
    session.commit()
    session.refresh(new_implemento)
    return new_implemento


def get_active_implements(session: Session):
    statement = select(ImplementoId).where(ImplementoId.activo == True)
    results = session.exec(statement).all()
    return results

def get_inactive_implements(session: Session):
    statement = select(ImplementoId).where(ImplementoId.activo == False)
    results = session.exec(statement).all()
    return results

def find_one_implement(id: int, session: Session):
    try:
        return session.get(ImplementoId, id)
    except NoResultFound:
        return None

def find_one_implement_category(categoria: str, session: Session):
    try:
        statement = select(ImplementoId).where(ImplementoId.categoria == categoria)
        result = session.exec(statement).first()
        return result
    except Exception:
        return None

def update_one_implement(id: int, new_implemento: ImplementoUpdate, session: Session):
    implemento_db = session.get(ImplementoId, id)

    if not implemento_db:
        return None

    try:
        update_data = new_implemento.model_dump(exclude_unset=True)

        implemento_db.sqlmodel_update(update_data)

        session.add(implemento_db)
        session.commit()
        session.refresh(implemento_db)
        return implemento_db

    except Exception as e:
        return None

def delete_implement(id: int, session: Session):
    implemento_db = session.get(ImplementoId, id)

    if not implemento_db:
        return None

    implemento_db.activo = False

    session.add(implemento_db)
    session.commit()
    session.refresh(implemento_db)

    return implemento_db

def reactivate_implement(id: int, session: Session):
    implemento_db = session.get(ImplementoId, id)

    if not implemento_db:
        return None

    statement = select(TurnoId).where(
        TurnoId.implemento_id == id,
        TurnoId.activo == True
    )
    turno_activo_con_implemento = session.exec(statement).first()

    if turno_activo_con_implemento:
        return None

    implemento_db.activo = True

    session.add(implemento_db)
    session.commit()
    session.refresh(implemento_db)

    return implemento_db



