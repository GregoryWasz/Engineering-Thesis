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
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/achievements".

    :param db: Sesja bazy danych
    :param current_user: użytkownik
    :return: Lista osiągnięć użytkownika
    """
    return get_all_user_achievements(db, current_user)


@achievement.get("/check")
def check_user_achievements(db: Session = Depends(get_db),
                            current_user: user_model.User = Depends(get_current_user)):
    """
    Tworzenie punktu końcowego metoda GET o adresie: "/achievements/check".

    :param db: Sesja bazy danych
    :param current_user: użytkownik
    :return: Informacja o nowych osiągnięciach lub ich braku
    """
    return check_achievements(db, current_user)
