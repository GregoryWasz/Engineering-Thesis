from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import post_model
from schemas.post import PostCreate


def get_posts_from_db(db: Session):
    return db.query(post_model.Post).all()


def create_post_in_db(post: PostCreate, db: Session, user_id: int):
    db_post = post_model.Post(user_id=user_id, **post.__dict__)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_single_post_by_post_id_from_db(post_id: int, db: Session):
    return db.query(post_model.Post).filter(post_model.Post.post_id == post_id).first()


def delete_post_from_db(post_id: int, db: Session):
    try:
        post = get_single_post_by_post_id_from_db(post_id, db)
        db.delete(post)
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def get_post_count_for_user_id(db: Session, user_id: int):
    return db.query(post_model.Post).filter(
        post_model.Post.user_id == user_id).count()
