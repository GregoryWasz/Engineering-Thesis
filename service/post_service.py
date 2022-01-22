from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from messages.messages import (
    PERMISSION_ERROR, POST_NOT_EXIST_ERROR, POST_DELETE_MESSAGE, DATABASE_ERROR,
)
from models import user_model
from repository.common_database_functions import apply_changes_and_refresh_db
from repository.post_repository import (
    get_posts_from_db, create_post_in_db, get_single_post_by_post_id_from_db,
    delete_post_from_db,
)
from schemas.post import PostCreate, PostNewTitle, PostNewText
from service.common_error_functions import _validate_text_length


def _raise_error_when_post_not_exist(post_id: int, db: Session):
    """
    Zwróć błąd jeśli wpis nie istnieje w bazie danych

    :param post_id: Identyfikator wpisu 
    :param db: Sesja bazy danych
    :return: Wpis
    """
    post = get_single_post_by_post_id_from_db(post_id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=POST_NOT_EXIST_ERROR,
        )

    return post


def _raise_error_when_user_is_not_post_owner(current_user_id: int, post_id: int, db: Session):
    """
    Zwróć błąd jeśli zalogowany użytkownik nie jest twórcą wpisu.

    :param current_user_id: Identyfikator użytkownika
    :param post_id: Identyfikator wpisu 
    :param db: Sesja bazy danych
    :return: None
    """
    post = _raise_error_when_post_not_exist(post_id, db)

    if current_user_id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=PERMISSION_ERROR,
        )


def get_posts(db: Session):
    """
    Pobieranie listy wszystkich wpisów.

    :param db: Sesja bazy danych
    :return: Lista wpisów
    """
    return get_posts_from_db(db)


def create_single_post(post: PostCreate, db: Session, current_user: user_model.User):
    """
    Tworzenie wpisu.
    Jeśli tekst lub tytuł wpisu jest za krótki zwróć błąd.

    :param post: Wpis
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Wpis
    """
    _validate_text_length(post.post_title)
    _validate_text_length(post.post_title)

    return create_post_in_db(post, db, current_user.user_id)


def get_single_post(post_id: int, db: Session):
    """
    Pobieranie wpisu.
    Jeśli wpis nie istnieje zwróć błąd.

    :param post_id: Identyfikator wpisu 
    :param db: Sesja bazy danych
    :return: Wpis
    """
    _raise_error_when_post_not_exist(post_id, db)
    return get_single_post_by_post_id_from_db(post_id, db)


def delete_post_with_id(post_id: int, db: Session, current_user: user_model.User):
    """
    Usuwanie wpisu.
    Jeśli zalogowany użytkownik nie jest twórcą wpisu zwróć błąd.

    :param post_id: Identyfikator wpisu 
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Potwierdzenie usunięcia
    """
    _raise_error_when_user_is_not_post_owner(current_user.user_id, post_id, db)

    if delete_post_from_db(post_id, db):
        return POST_DELETE_MESSAGE
    return DATABASE_ERROR


def update_post_title(post_id: int, post_title: PostNewTitle, db: Session, current_user: user_model.User):
    """
    Aktualizacja tytułu wpisu.
    Jeśli tytuł wpisu jest zbyt krótki zwróć błąd.
    Jeśli zalogowany użytkownik nie jest twórcą wpisu zwróć błąd.

    :param post_id: Identyfikator wpisu 
    :param post_title: Nowy tytuł wpisu
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Wpis
    """
    _raise_error_when_user_is_not_post_owner(current_user.user_id, post_id, db)

    _validate_text_length(post_title.post_title)

    post = get_single_post_by_post_id_from_db(post_id, db)
    post.post_title = post_title.post_title
    apply_changes_and_refresh_db(db, post)
    return post


def update_post_text(post_id: int, post_text: PostNewText, db: Session, current_user: user_model.User):
    """
    Aktualizacja tytułu wpisu.
    Jeśli tekst wpisu jest zbyt krótki zwróć błąd.
    Jeśli zalogowany użytkownik nie jest twórcą wpisu zwróć błąd.

    :param post_id: Identyfikator wpisu 
    :param post_text: Nowy tekst wpisu
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Wpis
    """
    _raise_error_when_user_is_not_post_owner(current_user.user_id, post_id, db)

    _validate_text_length(post_text.post_text)

    post = get_single_post_by_post_id_from_db(post_id, db)
    post.post_text = post_text.post_text
    apply_changes_and_refresh_db(db, post)
    return post
