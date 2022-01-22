from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from config import SECRET_KEY, ALGORITHM
from db.database import SessionLocal
from repository.user_repository import get_user
from schemas.token import TokenData


def get_db():
    """
    Utworzenie sesji z bazą danych

    :return: sesja bazy danych
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
"""
Utworzenie zabezpieczonego protokołem 0Auth2 punktu końcowego aplikacji do uwierzytelniania użytkowników
"""


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """

    :param token: token do uwierzytelniania użytkownika
    :param db: Sesja z bazą danych
    :return: obiekt użytkownika
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
