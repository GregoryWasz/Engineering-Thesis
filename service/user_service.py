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
    if len(user.username) < 4:
        _raise_http_exception(USERNAME_VALIDATION_ERROR)

    _check_if_calorie_value_is_lower_than_0(user.calorie_limit)
    _validate_email(user.email)
    _validate_password(user.password)

    _check_if_username_exist(db, user.username)
    _check_if_email_exist(db, user.email)

    user.password = hash_password(user.password)
    return user_repository.create_user(db=db, user=user)


def delete_user_service(db: Session, current_user):
    if user_repository.delete_user(db, current_user):
        return USER_DELETE_MESSAGE

    return _database_error()


def change_user_password(db: Session, current_user, new_password: user.UserUpdatePassword):
    _validate_password(new_password.password)

    hashed_new_password = hash_password(new_password.password)
    current_user.password = hashed_new_password

    if repository.common_database_functions.apply_changes_in_db(db):
        return PASSWORD_CHANGE_MESSAGE

    return _database_error()


def change_user_email(db: Session, current_user, new_email: user.UserUpdateEmail):
    _check_if_email_exist(db, new_email.email)
    _validate_email(new_email.email)

    current_user.email = new_email.email
    return repository.common_database_functions.apply_changes_in_db(db)


def change_user_username(db: Session, current_user, new_username: user.UserUpdateUsername):
    _check_if_username_exist(db, new_username.username)

    current_user.username = new_username.username
    return repository.common_database_functions.apply_changes_in_db(db)


def change_user_calorie_limit(db: Session, current_user, new_calorie_limit: user.UserUpdateCalorieLimit):
    _check_if_calorie_value_is_lower_than_0(new_calorie_limit.calorie_limit)
    current_user.calorie_limit = new_calorie_limit.calorie_limit
    return repository.common_database_functions.apply_changes_in_db(db)


def _check_if_username_exist(db: Session, username: str):
    if user_repository.get_user(db, username):
        return _raise_http_exception(USER_ALREADY_EXIST_ERROR)


def _check_if_email_exist(db: Session, email: str):
    if user_repository.get_user_by_email(db, email):
        return _raise_http_exception(EMAIL_ALREADY_EXIST_ERROR)


def _database_error():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=DATABASE_ERROR,
    )


def _validate_password(password: str):
    if len(password) < 10 and len(password) < 24:
        _raise_http_exception(PASSWORD_VALIDATION_ERROR)


def _validate_email(email: str):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(email_regex, email):
        _raise_http_exception(EMAIL_VALIDATION_ERROR)
