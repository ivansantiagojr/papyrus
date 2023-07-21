from fastapi import FastAPI

from .users.routes import router as users_router

app = FastAPI()
app.include_router(users_router, tags=['Users'])


@app.get('/')
def root():
    return {'message': 'ok'}
