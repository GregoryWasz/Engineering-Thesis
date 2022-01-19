from datetime import datetime

from pydantic import BaseModel

from schemas.user import UserBase


class Comment(BaseModel):
    comment_text: str
    comment_date: datetime

    class Config:
        orm_mode = True


class CommentResp(Comment):
    comment_id: int
    comment_creator: UserBase

    class Config:
        orm_mode = True


class CommentCreate(Comment):
    pass


class CommentNewText(BaseModel):
    comment_text: str
