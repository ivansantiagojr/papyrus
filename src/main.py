from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.auth.security import get_password_hash
from src.database import engine
from src.users.models import User

from .articles.routes import router as articles_router
from .auth.routes import router as auth_router
from .tags.routes import router as tags_router
from .users.routes import router as users_router

app = FastAPI()
app.include_router(users_router, tags=['Users'])
app.include_router(auth_router, tags=['Auth'])
app.include_router(articles_router, tags=['Articles'])
app.include_router(tags_router, tags=['Tags'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.on_event('startup')
async def startup_event():
    session = SessionLocal()
    db_user = session.scalar(select(User).where(User.username == 'admin'))
    if db_user:
        session.delete(db_user)
        session.commit()

    hashed_password = get_password_hash('admin')
    db_user = User(username='admin', password=hashed_password, role='ADMIN')
    session.add(db_user)
    session.commit()


@app.get('/')
def root():
    return {'message': 'ok'}
