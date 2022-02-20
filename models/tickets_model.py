from sqlalchemy import Column, Integer, String

from db.database import Base


class Ticket(Base):
    """
    Model dla bazy danych tworzący tabele Użytkownicy, wraz z odpowiednimi polami i relacjami.
    """
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
