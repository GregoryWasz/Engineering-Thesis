from pydantic import BaseModel

"""
Obiekty transferu danych dla modelu użytkownika.
"""


class UserBase(BaseModel):
    user_id: int
    username: str
    email: str
    calorie_limit: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    calorie_limit: int
    password: str


class UserRead(UserBase):
    user_id: int


class User(UserBase):
    pass


class UserUpdateEmail(BaseModel):
    email: str

    class Config:
        orm_mode = True


class UserUpdateUsername(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserUpdatePassword(BaseModel):
    password: str

    class Config:
        orm_mode = True


class UserUpdateCalorieLimit(BaseModel):
    calorie_limit: int

    class Config:
        orm_mode = True
