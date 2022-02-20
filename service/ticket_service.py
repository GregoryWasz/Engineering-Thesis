from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from messages.messages import TEXT_LENGTH_VALIDATION_ERROR
from repository.ticket_repository import get_tickets_from_db, create_ticket_in_db
from schemas.tickets import (
    CreateTicket
)


def get_tickets(db: Session):
    """
    Pobieranie listy biletów.

    :param db: Sesja bazy danych
    :return: Lista biletów
    """
    return get_tickets_from_db(db)


def create_single_ticket(ticket: CreateTicket, db: Session):
    """
    Dodawanie Biletu.
    Jeśli zawartość biletu będzie mniejsza od 4 zwróć błąd.

    :param ticket: Obiekt tworzonego biletu
    :param db: Sesja bazy danych
    :return: Dodany bilet
    """
    if len(ticket.message) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TEXT_LENGTH_VALIDATION_ERROR,
        )
    return create_ticket_in_db(ticket, db)
