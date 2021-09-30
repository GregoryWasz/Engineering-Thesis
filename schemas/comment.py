from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    comment_id: int
    comment_text: str
    comment_date: datetime
    # user_id: int
    # post_id: int
