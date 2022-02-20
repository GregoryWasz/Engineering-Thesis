from pydantic import BaseModel

"""
Obiekty transferu danych dla modelu pomiarów masy ciała.
"""


class NewAdminCredentials(BaseModel):
    username: str
    api_password: str

    class Config:
        orm_mode = True
