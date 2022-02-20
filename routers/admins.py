from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.admin import NewAdminCredentials
from service.admin_service import (
    promote_user_to_admin, admin_delete_post_with_id, admin_delete_comment_with_id, admin_delete_ticket_with_id,
)

admins = APIRouter()


@admins.put("/promote_to_admin")
def promote_to_admin(newAdminCredentials: NewAdminCredentials, db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/promote_to_admin".

    :param newAdminCredentials: Obiekt użytkownika i hasła do API
    :param db: Sesja bazy danych
    :return: Wiadomość o nadaniu roli
    """
    return promote_user_to_admin(newAdminCredentials, db)


@admins.delete("/{post_id:path}")
def admin_delete_post(post_id: int, db: Session = Depends(get_db),
                      current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/{post_id:path}".

    :param post_id: Identyfikator wpisu
    :param db: Sesja bazy danych
    :param current_user: użytkownik
    :return: Wiadomość o usunięciu wpisu
    """
    return admin_delete_post_with_id(post_id, db, current_user)


@admins.delete("/{comment_id:path}")
def admin_delete_comment(comment_id: int, db: Session = Depends(get_db),
                         current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/{comment_id:path}".

    :param comment_id: Identyfikator komentarza
    :param db: Sesja bazy danych
    :param current_user: użytkownik
    :return: Wiadomość o usunięciu komentarze
    """
    return admin_delete_comment_with_id(comment_id, db, current_user)


@admins.delete("/{ticket_id:path}")
def admin_delete_ticket(ticket_id: int, db: Session = Depends(get_db),
                        current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/{ticket_id:path}".

    :param ticket_id: Identyfikator biletu
    :param db: Sesja bazy danych
    :param current_user: użytkownik
    :return: Wiadomość o usunięciu biletu
    """
    return admin_delete_ticket_with_id(ticket_id, db, current_user)
