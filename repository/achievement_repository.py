from sqlalchemy.orm import Session

from models import achievement_model
from schemas.achievement import AchievementCreate


def get_all_achievements(db: Session, user_id: int):
    """
    Pobieranie z bazy danych wszystkich osiągnięć danego użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Lista osiągnięć dla wybranego użytkownika
    """
    return db.query(achievement_model.Achievement).filter(
        achievement_model.Achievement.user_id == user_id).all()


def get_achievement_count(db: Session, user_id: int):
    """
    Pobieranie z bazy danych ilości wszystkich osiągnięć danego użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Liczba całkowita
    """
    return db.query(achievement_model.Achievement).filter(
        achievement_model.Achievement.user_id == user_id).count()


def create_achievement_in_db(db: Session, user_id: int, achievement: AchievementCreate):
    """
    Tworzenie w bazie danych osiągnięcia.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :param achievement: Obiekt utworzenia osiągnięcia
    :return: Utworzone osiągnięcie
    """
    db_achievement = achievement_model.Achievement(user_id=user_id, **achievement.__dict__)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement
