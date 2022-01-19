from datetime import datetime

from pydantic import BaseModel

from schemas.user import UserBase


class Post(BaseModel):
    post_title: str
    post_text: str
    post_date: datetime

    class Config:
        orm_mode = True


class PostCreate(Post):
    pass


class PostCheck(Post):
    post_id: int
    user_id: int


class PostResp(Post):
    post_id: int
    user_id: int
    post_creator: UserBase

    class Config:
        orm_mode = True


class PostNewTitle(BaseModel):
    post_title: str

    class Config:
        orm_mode = True


class PostNewText(BaseModel):
    post_text: str

    class Config:
        orm_mode = True
