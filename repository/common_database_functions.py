from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def apply_changes_in_db(db: Session):
    """
    Zmiana wartości w bazie danych.

    :param db: Sesja bazy danych
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def apply_changes_and_refresh_db(db: Session, instance: Any):
    """
    Nadpisanie obiektu w bazie danych i odświeżenie jego wartości.

    :param db: Sesja bazy danych
    :param instance: Obiekt do zmiany
    :return:
    """
    apply_changes_in_db(db)
    db.refresh(instance)
