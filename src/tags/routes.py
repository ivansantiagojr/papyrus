from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.security import get_current_user
from src.database import get_session
from src.tags.models import Tag
from src.tags.schemas import TagPublic, TagSchema
from src.users.models import User

router = APIRouter(prefix='/tags')

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=TagPublic
)
def create_tag(tag: TagSchema, session: Session):
    db_tag = session.scalar(select(Tag).where(Tag.title == tag.title))

    if db_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Tag already exists',
        )

    db_tag = Tag(title=tag.title)

    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)

    return db_tag


@router.get('/', response_model=list[TagPublic])
def get_tags(session: Session):
    return session.scalars(select(Tag)).all()


@router.put('/{tag_id}', response_model=TagPublic)
def update_tag(
    tag_id: int,
    tag: TagSchema,
    session: Session,
):
    db_tag = session.scalar(select(Tag).where(Tag.id == tag_id))

    if not db_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Tag not found'
        )

    db_tag.title = tag.title
    session.commit()
    session.refresh(db_tag)

    return db_tag


@router.delete('/{tag_id}', response_model=TagPublic)
def delete_tag(tag_id: int, session: Session):
    db_tag = session.scalar(select(Tag).where(Tag.id == tag_id))

    if not db_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Tag not found'
        )

    session.delete(db_tag)
    session.commit()

    return db_tag
