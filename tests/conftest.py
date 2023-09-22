from datetime import datetime

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.articles.models import Article
from src.auth.security import get_password_hash
from src.database import Base, get_session
from src.main import app
from src.users.models import User


@pytest.fixture(scope='function')
def session():
    engine = create_engine(
        'postgresql+psycopg://postgres:testpassword@localhost:5435/postgres',
        pool_size=20,
        max_overflow=0,
    )

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)

    session = Session()
    session.begin()
    yield session

    session.rollback()
    session.close_all()

    Base.metadata.drop_all(engine)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.sequence(lambda n: n)
    username = factory.sequence(lambda n: f'test{n}')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}pass')
    role = 'WRITER'


class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    title = factory.Faker('text')
    content = factory.Faker('text')
    tags = factory.Faker('text')
    date = datetime.now()
    user_id = factory.SubFactory(UserFactory)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user = UserFactory(password=get_password_hash('test'))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.plain_password = 'test'

    return user


@pytest.fixture
def user2(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.plain_password = 'testtest'

    return user


@pytest.fixture
def admin_user(session):
    user = UserFactory(password=get_password_hash('test'), role='ADMIN')
    session.add(user)
    session.commit()
    session.refresh(user)

    user.plain_password = 'test'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.plain_password},
    )

    return response.json()['access_token']


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        '/token',
        data={
            'username': admin_user.username,
            'password': admin_user.plain_password,
        },
    )

    return response.json()['access_token']
