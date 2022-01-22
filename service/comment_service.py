from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from messages.messages import PERMISSION_ERROR, COMMENT_NOT_EXIST_ERROR, COMMENT_DELETE_MESSAGE, DATABASE_ERROR
from models import user_model
from repository.comment_repository import (
    create_comment_in_db, get_single_comment_by_comment_id_from_db,
    delete_comment_from_db, get_comments_by_post_id_from_db,
)
from repository.common_database_functions import apply_changes_and_refresh_db
from schemas.comment import (
    CommentCreate, CommentNewText,
)
from service.common_error_functions import _validate_text_length
from service.post_service import _raise_error_when_post_not_exist


def _when_comment_not_exist_raise_error(comment):
    """
    Zwróć błąd 400 jeżeli komentarz nie istnieje.

    :param comment: Komentarz 
    :return: None
    """
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=COMMENT_NOT_EXIST_ERROR,
        )


def _get_and_validate_comment(comment_id: int, db: Session):
    """
    Pobieranie komentarza.
    Jeśli nie istnieje w bazie danych zwróć błąd.

    :param comment_id: Identyfikator komentarza 
    :param db: Sesja bazy danych
    :return: Komentarz
    """
    comment = get_single_comment_by_comment_id_from_db(comment_id, db)
    _when_comment_not_exist_raise_error(comment)
    return comment


def _raise_error_when_user_is_not_comment_owner(current_user_id: int, comment_id: int, db: Session):
    """
    Zwróć błąd 401 jeśli zalogowany użytkownik nie jest twórcą komentarza.

    :param current_user_id: Identyfikator użytkownika
    :param comment_id: Identyfikator komentarza 
    :param db: Sesja bazy danych
    :return: None
    """
    comment = _get_and_validate_comment(comment_id, db)

    if current_user_id != comment.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=PERMISSION_ERROR,
        )


def create_single_comment(post_id: int, comment: CommentCreate, db: Session, current_user: user_model.User):
    """
    Tworzenie komentarza.
    Jeżeli treść komentarza jest za krótka zwróć błąd.

    :param post_id: Identyfikator wpisu
    :param comment: Komentarz 
    :param db: Sesja bazy danych
    :param current_user: Użytkownik 
    :return: Utworzony Komentarz
    """
    _raise_error_when_post_not_exist(post_id, db)
    _validate_text_length(comment.comment_text)

    return create_comment_in_db(post_id, comment, db, current_user.user_id)


def get_comments_for_post(post_id: int, db: Session):
    """
    Pobieranie komentarzy dla wpisu.

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych
    :return: Lista Komentarzy dla danego wpisu
    """
    return get_comments_by_post_id_from_db(post_id, db)


def delete_comment_with_id(comment_id: int, db: Session, current_user: user_model.User):
    """
    Usuwanie komentarza.
    Jeśli zalogowany użytkownik nie jest twórcą komentarza zwróć błąd.

    :param comment_id: Identyfikator komentarza 
    :param db: Sesja bazy danych
    :param current_user: Użytkownik Użytkownik 
    :return: Potwierdzenie usunięcia komentarza
    """
    _raise_error_when_user_is_not_comment_owner(current_user.user_id, comment_id, db)

    if delete_comment_from_db(comment_id, db):
        return COMMENT_DELETE_MESSAGE
    return DATABASE_ERROR


def update_comment_text(comment_id: int, new_comment_text: CommentNewText, db: Session, current_user: user_model.User):
    """
    Aktualizacja wartości tekstu.
    Jeśli tekst jest zbyt długi zwróć błąd.
    Jeśli zalogowany użytkownik nie jest twórcą komentarza zwróć błąd.

    :param comment_id: Identyfikator komentarza 
    :param new_comment_text: 
    :param db: Sesja bazy danych
    :param current_user: Użytkownik Użytkownik 
    :return: Zaktualizowany komentarz
    """
    _raise_error_when_user_is_not_comment_owner(current_user.user_id, comment_id, db)
    _validate_text_length(new_comment_text.comment_text)

    comment = get_single_comment_by_comment_id_from_db(comment_id, db)
    comment.comment_text = new_comment_text.comment_text
    apply_changes_and_refresh_db(db, comment)
    return comment
