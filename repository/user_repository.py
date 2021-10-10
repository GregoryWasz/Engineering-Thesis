from sqlalchemy.exc import SQLAlchemyError
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


def get_user(db: Session, username: str):
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def apply_changes_in_db(db: Session):
    try:
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def delete_user(db: Session, current_user):
    try:
        db.delete(current_user)
        db.commit()
    except SQLAlchemyError:
        return False
    return True
