import uvicorn
from fastapi import FastAPI

from db import database
from db.database import engine
from routers import users, authentication, body_weights, products, achievements, posts, comments

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.user_router, prefix='/users', tags=['users'])
app.include_router(authentication.auth, prefix='/auth', tags=['authentication'])
app.include_router(body_weights.body_weight, prefix='/body_weights', tags=['body_weights'])
app.include_router(products.products, prefix='/products', tags=['products'])
app.include_router(achievements.achievement, prefix='/achievements', tags=['achievements'])
app.include_router(posts.posts, prefix='/posts', tags=['posts'])
app.include_router(comments.comments, prefix='/comments', tags=['comments'])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
