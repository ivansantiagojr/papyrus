from datetime import datetime

from sqlalchemy import select

from src.articles.models import Article
from src.users.models import User
from src.users.schemas import UserRole


def test_create_user(session):
    new_user = User(username='ivan', password='1234', role=UserRole.admin)
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'ivan'))

    assert user.username == 'ivan'
    assert user.role == 'ADMIN'


def test_create_article(session, user):
    new_article = Article(
        title='Test article',
        content="Article's content",
        tags='tags',
        user_id=user.id,
        date=datetime.now(),
    )
    session.add(new_article)
    session.commit()

    article = session.scalar(select(Article).where(Article.user_id == user.id))

    assert article in user.articles
