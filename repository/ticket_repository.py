from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import tickets_model
from schemas.tickets import CreateTicket


def get_tickets_from_db(db: Session):
    """
    Pobieranie z bazy danych listy biletów.

    :param db: Sesja bazy danych
    :return: Lista Biletów
    """
    return db.query(tickets_model.Ticket).all()


def create_ticket_in_db(ticket: CreateTicket, db: Session):
    """
    Tworzenie biletu w bazie danych.

    :param ticket: Obiekt biletu
    :param db: Sesja bazy danych
    :return: Bilet
    """
    db_ticket = tickets_model.Ticket(**ticket.__dict__)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def delete_ticket_from_db(ticket_id: int, db: Session):
    """
    Usuwanie z bazy danych biletu.

    :param db: Sesja bazy danych
    :param ticket_id: Identyfikator biletu
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        comment = get_single_ticket_by_comment_id_from_db(ticket_id, db)
        db.delete(comment)
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def get_single_ticket_by_comment_id_from_db(ticket_id: int, db: Session):
    """
    Pobieranie biletu z bazy danych.

    :param ticket_id: Identyfikator biletu
    :param db: Sesja bazy danych
    :return: Bilet
    """
    return db.query(tickets_model.Ticket).filter(tickets_model.Ticket.ticket_id == ticket_id).first()
