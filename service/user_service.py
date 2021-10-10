from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from messages.messages import (
    USER_ALREADY_EXIST_ERROR, EMAIL_ALREADY_EXIST_ERROR, DATABASE_ERROR,
    PASSWORD_CHANGE_MESSAGE, USER_DELETE_MESSAGE,
)
from repository import user_repository
from schemas import user
from service.authentication import hash_password


def create_user_service(user: user.UserCreate, db: Session):
    _check_if_username_exist(db, user.username)
    _check_if_email_exist(db, user.email)

    user.password = hash_password(user.password)
    return user_repository.create_user(db=db, user=user)


def delete_user_service(db: Session, current_user):
    if user_repository.delete_user(db, current_user):
        return USER_DELETE_MESSAGE

    return _database_error()


def change_user_password(db: Session, current_user, new_password: user.UserUpdatePassword):
    hashed_new_password = hash_password(new_password.password)
    current_user.password = hashed_new_password

    if user_repository.apply_changes_in_db(db):
        return PASSWORD_CHANGE_MESSAGE

    return _database_error()


def change_user_email(db: Session, current_user, new_email: user.UserUpdateEmail):
    _check_if_email_exist(db, new_email.email)

    current_user.email = new_email.email
    return user_repository.apply_changes_in_db(db)


def change_user_username(db: Session, current_user, new_username: user.UserUpdateUsername):
    _check_if_username_exist(db, new_username.username)

    current_user.username = new_username.username
    return user_repository.apply_changes_in_db(db)


def _raise_http_exception(detail):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )


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
