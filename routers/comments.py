from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.comment import (
    CommentResp, CommentCreate, CommentNewText,
)
from service.comment_service import (
    create_single_comment, delete_comment_with_id, update_comment_text, get_comments_for_post,
)

comments = APIRouter()


@comments.post("/{post_id:path}", response_model=CommentResp)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db),
                   current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda POST o adresie: "/comments/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param comment: Komentarz
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Utworzony komentarz
    """
    return create_single_comment(post_id, comment, db, current_user)


@comments.get("/{post_id:path}", response_model=List[CommentResp])
def get_comments_for_post_with_id(post_id: int, db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda DELETE o adresie: "/comments/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych
    :return: Lista komentarzy dla danego wpisu
    """
    return get_comments_for_post(post_id, db)


@comments.delete("/{comment_id:path}")
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                   current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda DELETE o adresie: "/comments/{comment_id:path}".

    :param comment_id: Identyfikator komentarza
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Potwierdzenie utworzenia komentarza
    """
    return delete_comment_with_id(comment_id, db, current_user)


@comments.put("/text/{comment_id:path}", response_model=CommentResp)
def change_comment_text(comment_id: int, new_comment_text: CommentNewText, db: Session = Depends(get_db),
                        current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda DELETE o adresie: "/comments/text/{comment_id:path}".

    :param comment_id: Identyfikator komentarza
    :param new_comment_text: Nowa wartość tekstu komentarza
    :param db: Sesja bazy danych
    :param current_user: Użytkownik
    :return: Zaktualizowany komentarz
    """
    return update_comment_text(comment_id, new_comment_text, db, current_user)
