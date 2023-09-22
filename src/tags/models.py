from sqlalchemy.orm import Mapped, mapped_column  # , relationship

from src.database import Base


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
