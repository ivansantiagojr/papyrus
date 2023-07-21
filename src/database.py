from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from src.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


class Base(DeclarativeBase):
    pass


def get_session():
    with Session(engine) as session:
        yield session
