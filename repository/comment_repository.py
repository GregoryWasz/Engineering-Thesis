from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import comment_model
from schemas.comment import CommentCreate


def create_comment_in_db(post_id: int, comment: CommentCreate, db: Session, user_id: int):
    db_comment = comment_model.Comment(user_id=user_id, **comment.__dict__, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_single_comment_by_comment_id_from_db(comment_id: int, db: Session):
    return db.query(comment_model.Comment).filter(comment_model.Comment.comment_id == comment_id).first()


def delete_comment_from_db(comment_id: int, db: Session):
    try:
        comment = get_single_comment_by_comment_id_from_db(comment_id, db)
        db.delete(comment)
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def get_comment_count_for_user_id(db: Session, user_id: int):
    return db.query(comment_model.Comment).filter(
        comment_model.Comment.user_id == user_id).count()
