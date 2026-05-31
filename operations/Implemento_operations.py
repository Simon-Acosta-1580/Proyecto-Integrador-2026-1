from models import ImplementoBase, ImplementoId, ImplementoUpdate, TurnoId
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from typing import Optional

def createImplemento(implemento_data: ImplementoBase, session: Session, imagen_url: Optional[str] = None):
    statement = select(ImplementoId).where(ImplementoId.codigo == implemento_data.codigo)
    db_implemento = session.exec(statement).first()
    if db_implemento:
        return None

    new_implemento = ImplementoId(
        codigo=implemento_data.codigo,
        nombre=implemento_data.nombre,
        categoria=implemento_data.categoria,
        imagen=imagen_url
    )

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

def update_one_implement(id: int, implemento_data: ImplementoUpdate, session: Session, imagen_url: Optional[str] = None):
    implemento_db = session.get(ImplementoId, id)
    if not implemento_db:
        return None

    data_dict = implemento_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(implemento_db, key, value)

    if imagen_url:
        implemento_db.imagen = imagen_url

    session.add(implemento_db)
    session.commit()
    session.refresh(implemento_db)
    return implemento_db

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



