from typing import Generator
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, text
from sqlalchemy import create_engine

from config import settings


class Base(DeclarativeBase):
    pass


class Picture(Base):
    __tablename__ = "picture"
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    last_downloaded: Mapped[datetime | None]
    downloaded_qty: Mapped[int] = mapped_column(server_default="0")
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    processed: Mapped[datetime | None]
    extention: Mapped[str]

    def __repr__(self) -> str:
        return self.uuid


engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(engine)


def get_session() -> Generator:
    "Dependency to get session"
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
