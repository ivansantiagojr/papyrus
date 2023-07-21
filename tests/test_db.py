from sqlalchemy import select

from src.users.models import User
from src.users.schemas import UserRole


def test_create_user(session):
    new_user = User(username='ivan', password='1234', role=UserRole.admin)
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'ivan'))

    assert user.username == 'ivan'
    assert user.role == 'ADMIN'
