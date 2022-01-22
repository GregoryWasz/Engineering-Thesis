from datetime import datetime

from pydantic import BaseModel

"""
Obiekty transferu danych dla modelu osiągnięć.
"""


class Achievement(BaseModel):
    achievement_name: str
    achievement_date: datetime

    class Config:
        orm_mode = True


class AchievementCreate(Achievement):
    pass


class AchievementResponse(Achievement):
    achievement_id: int
