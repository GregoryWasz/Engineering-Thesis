from datetime import datetime
from datetime import timedelta
from typing import Optional

from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from config import SECRET_KEY, ALGORITHM
from messages.messages import INVALID_AUTHENTICATION
from repository.user_repository import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    """
    Hashowanie hasła.

    :param password: hasło
    :return: Hash hasła
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Porównywanie haseł.

    :param plain_password: hasło
    :param hashed_password: hasło
    :return: Wartość boolowska Prawda/Fałsz
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(get_db, username: str, password: str):
    """
    Uwierzytelnianie użytkownika.

    :param get_db: Sesja bazy danych
    :param username: Nazwa użytkownika
    :param password: Hasło użytkownika
    :return: Any
    """
    user = get_user(get_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Utworzenie tokenu dostępowego dla aplikacji.

    :param data: Data
    :param expires_delta: Czas wygaśnięcia
    :return: Token dostępowy do aplikacji
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    """
    Uwierzytelnienie użytkownika.
    Utworzenie tokenu dostępowego.

    :param form_data:
    :param db: Sesja bazy danych
    :return: Token dostępowy do aplikacji
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_AUTHENTICATION,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "admin": user.admin}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
