from fastapi import FastAPI
import uvicorn

from db.database import engine
from routers import users
from db import database

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.user_router, prefix='/users', tags=['users'])


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
