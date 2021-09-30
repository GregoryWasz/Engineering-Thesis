from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db
from repository import user_repository
from schemas import user

user_router = APIRouter()


@user_router.get("/", response_model=List[user.UserBase])
def read_users_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_repository.get_users(db, skip=skip, limit=limit)
    return users


@user_router.post("/", response_model=user.UserBase)
def create_user_api(user: user.UserCreate, db: Session = Depends(get_db)):
    return user_repository.create_user(db=db, user=user)
