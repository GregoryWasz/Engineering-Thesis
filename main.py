import uvicorn
from fastapi import FastAPI

from db import database
from db.database import engine
from routers import users, authentication

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.user_router, prefix='/users', tags=['users'])
app.include_router(authentication.auth, prefix='/auth', tags=['authentication'])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
