from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from repository import user_repository
from schemas import user
from service.user_service import (
    create_user_service, delete_user_service, change_user_password, change_user_email,
    change_user_username, change_user_calorie_limit,
)

user_router = APIRouter()


@user_router.get("", response_model=List[user.UserBase])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/users".

    :param skip: Przesunięcie
    :param limit: Ograniczenie listy
    :param db: Sesja bazy danych  
    :return: Lista użytkowników
    """
    return user_repository.get_users(db=db, skip=skip, limit=limit)


@user_router.post("", response_model=user.UserBase)
def create_user_api(user: user.UserCreate, db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda POST o adresie: "/users".
    
    :param user: Użytkownik
    :param db: Sesja bazy danych  
    :return: Użytkownik
    """
    return create_user_service(db=db, user=user)


@user_router.delete("")
def delete_user(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda DELETE o adresie: "/users".
    
    :param db: Sesja bazy danych  
    :param current_user: Użytkownik 
    :return: Potwierdzenie usunięcia użytkownika
    """
    return delete_user_service(db, current_user)


@user_router.put("/password")
def change_password(new_password: user.UserUpdatePassword, db: Session = Depends(get_db),
                    current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda PUT o adresie: "/users/password".

    :param new_password: Nowe hasło
    :param db: Sesja bazy danych  
    :param current_user: Użytkownik 
    :return: Potwierdzenie zmiany hasła
    """
    return change_user_password(db, current_user, new_password)


@user_router.put("/email")
def change_email(new_email: user.UserUpdateEmail, db: Session = Depends(get_db),
                 current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda PUT o adresie: "/users/email".
    
    :param new_email: Nowy adres email
    :param db: Sesja bazy danych  
    :param current_user: Użytkownik 
    :return: Potwierdzenie zmiany adresu email
    """
    return change_user_email(db, current_user, new_email)


@user_router.put("/username")
def change_username(new_username: user.UserUpdateUsername, db: Session = Depends(get_db),
                    current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda PUT o adresie: "/users/username".
    
    :param new_username: Nowa nazwa użytkownika
    :param db: Sesja bazy danych  
    :param current_user: Użytkownik 
    :return: Potwierdzenie zmiany nazwy użytkownika
    """
    return change_user_username(db, current_user, new_username)


@user_router.put("/calorie")
def change_calorie_limit(new_calorie_limit: user.UserUpdateCalorieLimit, db: Session = Depends(get_db),
                         current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda PUT o adresie: "/users/calorie".

    :param new_calorie_limit: Nowa ilość kalorii
    :param db: Sesja bazy danych  
    :param current_user: Użytkownik 
    :return: Potwierdzenie zmiany limitu kalorii
    """
    return change_user_calorie_limit(db, current_user, new_calorie_limit)
