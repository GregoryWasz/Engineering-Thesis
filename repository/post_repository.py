from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import post_model
from schemas.post import PostCreate


def get_posts_from_db(db: Session):
    """
    Pobieranie wpisów z bazy danych.

    :param db: Sesja bazy danych
    :return: Lista wpisów
    """
    return db.query(post_model.Post).order_by(post_model.Post.post_date.desc()).all()


def create_post_in_db(post: PostCreate, db: Session, user_id: int):
    """
    Tworzenie wpisu w bazie danych.

    :param post: Obiekt wpisu
    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Wpis
    """
    db_post = post_model.Post(user_id=user_id, **post.__dict__)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_single_post_by_post_id_from_db(post_id: int, db: Session):
    """
    Pobieranie wpisu z bazy danych.

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych
    :return: Wpis
    """
    return db.query(post_model.Post).filter(post_model.Post.post_id == post_id).first()


def delete_post_from_db(post_id: int, db: Session):
    """
    Usuwanie z bazy danych komentarza.

    :param db: Sesja bazy danych
    :param post_id: Identyfikator wpis
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        post = get_single_post_by_post_id_from_db(post_id, db)
        db.delete(post)
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def get_post_count_for_user_id(db: Session, user_id: int):
    """
    Pobieranie ilości wpisu z bazy danych dla danego użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Liczba całkowita
    """
    return db.query(post_model.Post).filter(
        post_model.Post.user_id == user_id).count()
