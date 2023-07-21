from enum import Enum

from pydantic import BaseModel, ConfigDict


class UserRole(str, Enum):
    admin = 'ADMIN'
    writer = 'WRITER'


class UserSchema(BaseModel):
    username: str
    password: str
    role: UserRole


class UserPublic(BaseModel):
    id: int
    username: str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class Message(BaseModel):
    detail: str
