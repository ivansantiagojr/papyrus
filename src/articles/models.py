from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.tags.models import Tag
    from src.users.models import User


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    # write a tags field that is a list of Tag objects
    # tags: Mapped[list[int]] = mapped_column(ForeignKey("tags.id"))
    tags: Mapped[str]
    date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="articles")
    # tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="articles")
