from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    post_id: int
    post_title: str
    post_text: str
    post_date: datetime
    # user_id: int
