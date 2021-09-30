from sqlalchemy.orm import Session

from models import user_model
from schemas import user


def create_user(db: Session, user: user.UserCreate):
    db_user = user_model.User(username=user.username, password=user.password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()
