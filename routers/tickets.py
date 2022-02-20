from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db
from schemas.tickets import (
    Ticket, CreateTicket,
)
from service.ticket_service import (
    get_tickets, create_single_ticket,
)

tickets = APIRouter()


@tickets.get("", response_model=List[Ticket])
def get_all_tickets(db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/tickets".

    :param db: Sesja bazy danych
    :return: Lista biletów
    """
    return get_tickets(db)


@tickets.post("", response_model=Ticket)
def create_ticket(ticket: CreateTicket, db: Session = Depends(get_db)):
    """
    Tworzenie punktu końcowego metoda POST o adresie: "/tickets".

    :param ticket: Bilet
    :param db: Sesja bazy danych
    :return: Utworzony bilet
    """
    return create_single_ticket(ticket, db)
