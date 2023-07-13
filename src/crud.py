from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from db import Picture


def create_picture(session: Session, extention: str) -> str:
    picture = Picture(extention=extention)
    session.add(picture)
    session.commit()
    return picture.uuid


def get_picture_by_uuid(
    uuid: str, session: Session, *, only_downloaded_qty=False
) -> Picture | None:
    select_statement = Picture if not only_downloaded_qty else Picture.downloaded_qty
    query = select(select_statement).where(Picture.uuid == uuid)
    return session.scalars(query).first()


def update_picture_is_downloaded_by_uuid(uuid: str, session: Session) -> None:
    downloaded_qty = get_picture_by_uuid(uuid, session, only_downloaded_qty=True)
    query = (
        update(Picture)
        .where(Picture.uuid == uuid)
        .values(last_downloaded=datetime.now(), downloaded_qty=downloaded_qty + 1)
    )
    session.execute(query)
    session.commit()


def get_all_pictures(session: Session) -> list[Picture]:
    query = select(Picture)
    return session.scalars(query).all()
