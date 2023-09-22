from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.articles.models import Article
from src.articles.schemas import (
    ArticlePublic,
    ArticleSchema,
    ArticleUpdate,
    Message,
)
from src.auth.security import get_current_user
from src.database import get_session
from src.users.models import User

router = APIRouter(prefix='/articles')

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=ArticlePublic)
def create_article(
    article: ArticleSchema, user: CurrentUser, session: Session
):
    db_article = Article(**article.model_dump(), user_id=user.id)

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    return db_article


@router.get('/', response_model=list[ArticlePublic])
def get_articles(
    session: Session,
    title: str | None = None,
    content: str | None = None,
    user_id: int | None = None,
    tags: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = select(Article)
    if tags:
        query = query.filter(Article.tags.contains(tags))

    if title:
        query = query.filter(Article.title.contains(title))

    if content:
        query = query.filter(Article.content.contains(content))

    if user_id:
        query = query.filter(Article.user_id == user_id)

    articles = session.scalars(query.offset(skip).limit(limit)).all()

    return articles


@router.put('/{article_id}', response_model=ArticlePublic)
def update_article(
    article_id: int,
    session: Session,
    user: CurrentUser,
    article: ArticleUpdate,
):
    db_article = session.scalar(
        select(Article).filter(Article.id == article_id)
    )

    if not db_article:
        raise HTTPException(status_code=404, detail='Article not found')

    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    return db_article


@router.delete('/{article_id}', response_model=Message)
def delete_article(article_id: int, session: Session, user: CurrentUser):
    if user.role != 'ADMIN':
        raise HTTPException(status_code=403, detail='Not enough permissions')

    db_article = session.scalar(
        select(Article).filter(Article.id == article_id)
    )

    if not db_article:
        raise HTTPException(status_code=404, detail='Article not found')

    session.delete(db_article)
    session.commit()

    return {'detail': 'Article deleted'}
