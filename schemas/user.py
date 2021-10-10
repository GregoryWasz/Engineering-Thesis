from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
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
