import re

from fastapi import status, HTTPException
from sqlalchemy.orm import Session

import repository.common_database_functions
from messages.messages import (
    USER_ALREADY_EXIST_ERROR, EMAIL_ALREADY_EXIST_ERROR, DATABASE_ERROR,
    PASSWORD_CHANGE_MESSAGE, USER_DELETE_MESSAGE, USERNAME_VALIDATION_ERROR, EMAIL_VALIDATION_ERROR,
    PASSWORD_VALIDATION_ERROR,
)
from repository import user_repository
from schemas import user
from service.authentication import hash_password
from service.common_error_functions import _raise_http_exception, _check_if_calorie_value_is_lower_than_0


def create_user_service(user: user.UserCreate, db: Session):
    """
    Utworzenie użytkownika.
    Jeśli wartość kalorii jest niepoprawna zwróć błąd.
    Jeśli nazwa użytkownika jest niepoprawna zwróć błąd.
    Jeśli hasło jest niepoprawne zwróć błąd.
    Jeśli adres email jest niepoprawny zwróć błąd.

    :param user: Użytkownik
    :param db: Sesja Bazy danych 
    :return: Stworzony użytkownik
    """
    _check_if_calorie_value_is_lower_than_0(user.calorie_limit)
    _validate_username(user.username)
    _validate_email(user.email)
    _validate_password(user.password)

    _check_if_username_exist(db, user.username)
    _check_if_email_exist(db, user.email)

    user.password = hash_password(user.password)
    return user_repository.create_user(db=db, user=user)


def delete_user_service(db: Session, current_user):
    """
    Usuwanie użytkownika.

    :param db: Sesja Bazy danych 
    :param current_user: Użytkownik 
    :return: Potwierdzenie usunięcia
    """
    if user_repository.delete_user(db, current_user):
        return USER_DELETE_MESSAGE

    return _database_error()


def change_user_password(db: Session, current_user, new_password: user.UserUpdatePassword):
    """
    Jeśli hasło jest niepoprawne zwróć błąd.

    :param db: Sesja Bazy danych 
    :param current_user: Użytkownik 
    :param new_password: Nowe hasło
    :return: Potwierdzenie zmiany
    """
    _validate_password(new_password.password)

    hashed_new_password = hash_password(new_password.password)
    current_user.password = hashed_new_password

    if repository.common_database_functions.apply_changes_in_db(db):
        return PASSWORD_CHANGE_MESSAGE

    return _database_error()


def change_user_email(db: Session, current_user, new_email: user.UserUpdateEmail):
    """
    Aktualizacja adresu email.
    Jeśli adres email jest niepoprawny zwróć błąd.

    :param db: Sesja Bazy danych 
    :param current_user: Użytkownik
    :param new_email: Nowy Adres email
    :return: Potwierdzenie zmiany
    """
    _check_if_email_exist(db, new_email.email)
    _validate_email(new_email.email)

    current_user.email = new_email.email
    return repository.common_database_functions.apply_changes_in_db(db)


def change_user_username(db: Session, current_user, new_username: user.UserUpdateUsername):
    """
    Aktualizacja nazwy użytkownika.
    Jeśli nazwa użytkownika jest niepoprawna zwróć błąd.

    :param db: Sesja Bazy danych 
    :param current_user: Użytkownik 
    :param new_username: Nowa nazwa użytkownika
    :return: Potwierdzenie zmiany
    """
    _check_if_username_exist(db, new_username.username)
    _validate_username(new_username.username)

    current_user.username = new_username.username
    return repository.common_database_functions.apply_changes_in_db(db)


def change_user_calorie_limit(db: Session, current_user, new_calorie_limit: user.UserUpdateCalorieLimit):
    """
    Aktualizacja limitu kalorycznego.
    Jeśli wartość kalorii jest niepoprawna zwróć błąd.

    :param db: Sesja Bazy danych 
    :param current_user: Użytkownik 
    :param new_calorie_limit: Nowy limit kalorii
    :return: Potwierdzenie zmiany
    """
    _check_if_calorie_value_is_lower_than_0(new_calorie_limit.calorie_limit)
    current_user.calorie_limit = new_calorie_limit.calorie_limit
    return repository.common_database_functions.apply_changes_in_db(db)


def _check_if_username_exist(db: Session, username: str):
    """
    Walidacja czy nazwa użytkownika istnieje.
    
    :param db: Sesja bazy danych
    :param username: nazwa użytkownika
    :return: 
    """
    if user_repository.get_user(db, username):
        return _raise_http_exception(USER_ALREADY_EXIST_ERROR)


def _check_if_email_exist(db: Session, email: str):
    """
    Walidacja czy adres email istnieje.
    
    :param db: Sesja bazy danych
    :param email: adres email
    :return: None
    """
    if user_repository.get_user_by_email(db, email):
        return _raise_http_exception(EMAIL_ALREADY_EXIST_ERROR)


def _database_error():
    """
    Błąd bazy danych.
    
    :return: None 
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=DATABASE_ERROR,
    )


def _validate_username(username: str):
    """
    Walidacja nazwy użytkownika.
    
    
    :param username: nazwa użytkownika
    :return: None
    """
    if len(username) < 4 or len(username) > 16:
        _raise_http_exception(USERNAME_VALIDATION_ERROR)


def _validate_password(password: str):
    """
    Walidacja hasła.
    
    :param password: hasło
    :return: None
    """
    if len(password) < 10 or len(password) > 24:
        _raise_http_exception(PASSWORD_VALIDATION_ERROR)


def _validate_email(email: str):
    """
    Walidacja adresu email.
    
    :param email: adres email
    :return: None
    """
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(email_regex, email):
        _raise_http_exception(EMAIL_VALIDATION_ERROR)
