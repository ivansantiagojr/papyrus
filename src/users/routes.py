from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.users.models import User
from src.users.schemas import Message, UserPublic, UserSchema

router = APIRouter()


@router.post('/users', status_code=201, response_model=UserPublic)
def create_user(
    user: UserSchema, session: Session = Depends(get_session)
) -> Any:
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(status_code=400, detail='Username already used')

    db_user = User(
        username=user.username, password=user.password, role=user.role
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/users', response_model=list[UserPublic])
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> Any:
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users


@router.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
) -> Any:
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.password = user.password
    db_user.role = user.role

    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)) -> Any:
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}
