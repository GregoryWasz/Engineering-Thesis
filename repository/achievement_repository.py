from sqlalchemy.orm import Session

from models import achievement_model
from schemas.achievement import AchievementCreate


def get_all_achievements(db: Session, user_id: int):
    return db.query(achievement_model.Achievement).filter(
        achievement_model.Achievement.user_id == user_id).all()


def get_achievement_count(db: Session, user_id: int):
    return db.query(achievement_model.Achievement).filter(
        achievement_model.Achievement.user_id == user_id).count()


def create_achievement(db: Session, user_id: int, achievement: AchievementCreate):
    db_achievement = achievement_model.Achievement(user_id=user_id, **achievement.__dict__)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement
