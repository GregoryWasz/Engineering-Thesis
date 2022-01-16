import uvicorn
from fastapi import FastAPI

from db import database
from db.database import engine
from routers import users, authentication, body_weights, products, achievements, posts, comments
from fastapi.middleware.cors import CORSMiddleware

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.user_router, prefix='/users', tags=['users'])
app.include_router(authentication.auth, prefix='/auth', tags=['authentication'])
app.include_router(body_weights.body_weight, prefix='/body_weights', tags=['body_weights'])
app.include_router(products.products, prefix='/products', tags=['products'])
app.include_router(achievements.achievement, prefix='/achievements', tags=['achievements'])
app.include_router(posts.posts, prefix='/posts', tags=['posts'])
app.include_router(comments.comments, prefix='/comments', tags=['comments'])

origins = [
    "http://localhost",
    "http://localhost",
    "http://localhost:3000",
    "localhost",
    "localhost:3000",
    "https://localhost",
    "https://localhost:3000",
    "http://localhost:5000",
    "https://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
