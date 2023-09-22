from pydantic import BaseModel


class TagSchema(BaseModel):
    title: str


class TagPublic(TagSchema):
    id: int
