from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import comment_model
from schemas.comment import CommentCreate


def create_comment_in_db(post_id: int, comment: CommentCreate, db: Session, user_id: int):
    """
    Tworzenie komentarza w bazie danych.

    :param post_id: Identyfikator wpisu
    :param comment: Obiekt komentarza
    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Komentarz
    """
    db_comment = comment_model.Comment(user_id=user_id, **comment.__dict__, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_single_comment_by_comment_id_from_db(comment_id: int, db: Session):
    """
    Pobieranie komentarza z bazy danych.

    :param comment_id: Identyfikator komentarza
    :param db: Sesja bazy danych
    :return: Komentarz
    """
    return db.query(comment_model.Comment).filter(comment_model.Comment.comment_id == comment_id).first()


def get_comments_by_post_id_from_db(post_id: int, db: Session):
    """
    Pobieranie wszystkich komentarzy z bazy danych dla danego wpisu.

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych
    :return: Lista komentarzy
    """
    return db.query(comment_model.Comment).filter(comment_model.Comment.post_id == post_id).all()


def delete_comment_from_db(comment_id: int, db: Session):
    """
    Usuwanie z bazy danych komentarza.

    :param db: Sesja bazy danych
    :param comment_id: Identyfikator komentarza
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        comment = get_single_comment_by_comment_id_from_db(comment_id, db)
        db.delete(comment)
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def get_comment_count_for_user_id(db: Session, user_id: int):
    """
    Pobieranie z bazy danych liczby komentarzy dla danego użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Liczba całkowita
    """
    return db.query(comment_model.Comment).filter(
        comment_model.Comment.user_id == user_id).count()
