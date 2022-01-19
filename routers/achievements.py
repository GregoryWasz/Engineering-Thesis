from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.achievement import AchievementResponse
from service.achievement_service import (
    get_all_user_achievements, check_achievements,
)

achievement = APIRouter()


@achievement.get("", response_model=List[AchievementResponse])
def get_user_achievements(db: Session = Depends(get_db),
                          current_user: user_model.User = Depends(get_current_user)):
    return get_all_user_achievements(db, current_user)


@achievement.get("/check")
def check_user_achievements(db: Session = Depends(get_db),
                            current_user: user_model.User = Depends(get_current_user)):
    return check_achievements(db, current_user)
