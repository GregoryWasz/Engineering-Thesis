from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import repository.common_database_functions
from config import SECRET_ADMIN_KEY
from models.user_model import User
from repository.comment_repository import delete_comment_from_db
from repository.post_repository import delete_post_from_db
from repository.ticket_repository import delete_ticket_from_db
from repository.user_repository import get_user, get_user_by_email
from schemas.admin import NewAdminCredentials, NewUserPassword
from service.authentication import hash_password
from service.user_service import _validate_password


def promote_user_to_admin(newAdminCredentials: NewAdminCredentials, db: Session):
    """
    Nadanie roli administratora danemu użytkownikowi.
    Jeśli nazwa użytkownika nie istnieje zwróć błąd.
    Jeśli hasło jest niepoprawne zwróć błąd.

    :param newAdminCredentials: Obiekt przechowujący klucz i nazwę nowego administratora
    :param db: Sesja bazy danych
    :return: Wiadomość o promocji do roli administratora
    """

    user = get_user(db, newAdminCredentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if newAdminCredentials.api_password != SECRET_ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong Api Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.admin = True
    repository.common_database_functions.apply_changes_in_db(db)
    return {"message": f"{user.username} successfully promoted to admin"}


def change_user_password(newUserPassword: NewUserPassword, db: Session, current_user: User):
    """
    Zmiana hasła dla danego użytkownika
    Jeśli nazwa użytkownika nie istnieje zwróć błąd.
    Jeśli hasło jest niepoprawne zwróć błąd.

    :param current_user: Zalogowany użytkownik
    :param newUserPassword: Obiekt przechowujący hasło i nazwę użytkownika
    :param db: Sesja bazy danych
    :return: Wiadomość o promocji do roli administratora
    """
    _check_admin_role(current_user)
    user = get_user_by_email(db, newUserPassword.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    _validate_password(newUserPassword.password)

    hashed_new_password = hash_password(newUserPassword.password)
    user.password = hashed_new_password

    repository.common_database_functions.apply_changes_in_db(db)
    return {"message": f"Password for: {user.username} successfully changed"}


def admin_delete_post_with_id(post_id: int, db: Session, current_user: User):
    """
    Usunięcie wpisu o danym identyfikatorze przez administratora.
    Jeśli użytkownik nie jest administratorem zwróć błąd.

    :param post_id: Obiekt przechowujący klucz i nazwę nowego administratora
    :param db: Sesja bazy danych
    :param current_user: Zalogowany użytkownik
    :return: Wiadomość o usunięciu
    """
    _check_admin_role(current_user)
    return delete_post_from_db(post_id, db)


def admin_delete_comment_with_id(comment_id: int, db: Session, current_user: User):
    """
    Usunięcie komentarza o danym identyfikatorze przez administratora.
    Jeśli użytkownik nie jest administratorem zwróć błąd.

    :param comment_id: Obiekt przechowujący klucz i nazwę nowego administratora
    :param db: Sesja bazy danych
    :param current_user: Zalogowany użytkownik
    :return: Wiadomość o usunięciu
    """
    _check_admin_role(current_user)
    return delete_comment_from_db(comment_id, db)


def admin_delete_ticket_with_id(ticket_id: int, db: Session, current_user: User):
    """
    Usunięcie blietu o danym identyfikatorze przez administratora.
    Jeśli użytkownik nie jest administratorem zwróć błąd.

    :param ticket_id: Obiekt przechowujący klucz i nazwę nowego administratora
    :param db: Sesja bazy danych
    :param current_user: Zalogowany użytkownik
    :return: Wiadomość o usunięciu
    """
    _check_admin_role(current_user)
    return delete_ticket_from_db(ticket_id, db)


def _check_admin_role(user: User):
    """
    Funkcja sprawdzająca role użytkownika
    Jeśli użytkownik nie jest administratorem zwróć błąd.

    :param user: Obiekt użytkownika
    """
    if not user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
