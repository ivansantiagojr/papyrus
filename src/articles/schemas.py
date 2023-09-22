from datetime import datetime

from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    content: str
    tags: str
    date: datetime


class ArticlePublic(ArticleSchema):
    id: int
    user_id: int


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: str | None = None
    date: datetime | None = None


class Message(BaseModel):
    detail: str
