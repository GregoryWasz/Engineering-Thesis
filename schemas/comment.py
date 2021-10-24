from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    comment_text: str
    comment_date: datetime

    class Config:
        orm_mode = True


class CommentResp(Comment):
    comment_id: int


class CommentCreate(Comment):
    pass


class CommentNewText(BaseModel):
    comment_text: str
