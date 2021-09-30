from datetime import datetime

from pydantic import BaseModel


class Achievement(BaseModel):
    achievement_id: int
    achievement_name: str
    achievement_date: datetime
    # user_id: int
