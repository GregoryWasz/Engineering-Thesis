from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import user_model
from schemas import user


def create_user(db: Session, user: user.UserCreate):
    """
    Tworzenie użytkownika w bazie danych.

    :param user: Obiekt użytkownika
    :param db: Sesja bazy danych
    :return: Produkt
    """
    db_user = user_model.User(**user.__dict__)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Pobieranie listy użytkowników z bazy danych.

    :param db: Sesja bazy danych
    :param skip: Przesunięcie
    :param limit: Ograniczenie listy
    :return: Lista użytkowników
    """
    return db.query(user_model.User).offset(skip).limit(limit).all()


def get_user(db: Session, username: str):
    """
    Pobieranie użytkownika z bazy danych za pomocą jego nazwy.

    :param db: Sesja bazy danych
    :param username: Nazwa użytkownika
    :return: Użytkownik
    """
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """
    Pobieranie użytkownika z bazy danych za pomocą jego adresu e-mail.

    :param db: Sesja bazy danych
    :param email: Adres email
    :return: Użytkownik
    """
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def delete_user(db: Session, current_user):
    """
    Usuwanie z bazy użytkownika.

    :param db: Sesja bazy danych
    :param current_user: użytkownik
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        db.delete(current_user)
        db.commit()
    except SQLAlchemyError:
        return False
    return True
