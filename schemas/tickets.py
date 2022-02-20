from pydantic import BaseModel

"""
Obiekty transferu danych dla modelu biletów.
"""


class Ticket(BaseModel):
    ticket_id: int
    message: str

    class Config:
        orm_mode = True


class CreateTicket(BaseModel):
    message: str

    class Config:
        orm_mode = True
