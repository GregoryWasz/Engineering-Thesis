from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.post import (
    PostResp, PostCreate, PostNewText, PostNewTitle,
)
from service.post_service import (
    get_posts, get_single_post, create_single_post, delete_post_with_id, update_post_title,
    update_post_text,
)

posts = APIRouter()


@posts.get("", response_model=List[PostResp])
def get_all_posts(db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/posts".

    :param db: Sesja bazy danych 
    :return: Lista wpisów
    """
    return get_posts(db)


@posts.post("", response_model=PostResp)
def create_post(post: PostCreate, db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda POST o adresie: "/posts".

    :param post: Wpis
    :param db: Sesja bazy danych 
    :param current_user: Użytkownik 
    :return: Utworzony wpis
    """
    return create_single_post(post, db, current_user)


@posts.get("/{post_id:path}", response_model=PostResp)
def get_post_with_id(post_id: int, db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/posts/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych 
    :return: Wpis
    """
    return get_single_post(post_id, db)


@posts.delete("/{post_id:path}")
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda DELETE o adresie: "/posts/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych 
    :param current_user: Użytkownik 
    :return: Potwierdzenie usunięcia wpisu
    """
    return delete_post_with_id(post_id, db, current_user)


@posts.put("/title/{post_id:path}", response_model=PostResp)
def change_post_title(post_id: int, post_title: PostNewTitle, db: Session = Depends(get_db),
                      current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda PUT o adresie: "/title/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param post_title: Nowy tytuł wpisu
    :param db: Sesja bazy danych 
    :param current_user: Użytkownik 
    :return: Zaktualizowany wpis
    """
    return update_post_title(post_id, post_title, db, current_user)


@posts.put("/text/{post_id:path}", response_model=PostResp)
def change_post_text(post_id: int, post_text: PostNewText, db: Session = Depends(get_db),
                     current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda PUT o adresie: "/text/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param post_text: Nowy tekst wpisu
    :param db: Sesja bazy danych 
    :param current_user: Użytkownik 
    :return: Zaktualizowany wpis
    """
    return update_post_text(post_id, post_text, db, current_user)
