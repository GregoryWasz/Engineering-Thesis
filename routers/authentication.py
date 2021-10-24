from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from schemas import user
from schemas.token import Token
from service.authentication import get_access_token

auth = APIRouter()


@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return get_access_token(form_data, db)


@auth.get("/me", response_model=user.UserBase)
async def read_users_me(current_user: user = Depends(get_current_user)):
    return current_user
