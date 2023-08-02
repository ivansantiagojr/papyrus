from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.security import get_current_user, get_password_hash
from src.database import get_session
from src.users.models import User
from src.users.schemas import Message, UserPublic, UserSchema

router = APIRouter(prefix='/users')
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=201, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
) -> Any:
    if current_user.role != 'ADMIN':
        raise HTTPException(status_code=403, detail='Not allowed')

    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(status_code=400, detail='Username already used')

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, role=user.role
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=list[UserPublic])
def get_users(
    session: Session,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    if current_user.role != 'ADMIN':
        raise HTTPException(status_code=403, detail='Not allowed')

    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
) -> Any:
    if current_user.id != user_id and current_user.role != 'ADMIN':
        raise HTTPException(status_code=403, detail='Not allowed')

    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.password = user.password

    if current_user.role == 'ADMIN':
        db_user.role = user.role

    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
) -> Any:
    if current_user.id != user_id and current_user.role != 'ADMIN':
        raise HTTPException(status_code=403, detail='Not allowed')

    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}
