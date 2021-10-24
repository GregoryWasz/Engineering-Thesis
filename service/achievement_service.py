from datetime import datetime

from sqlalchemy.orm import Session

from messages.messages import NO_NEW_ACHIEVEMENTS_MESSAGE, NEW_ACHIEVEMENTS_MESSAGE
from models import user_model
from repository.achievement_repository import (
    get_all_achievements, get_achievement_count,
    create_achievement_in_db,
)
from repository.body_weight_repository import get_measurement_count_for_user_id
from repository.comment_repository import get_comment_count_for_user_id
from repository.post_repository import get_post_count_for_user_id
from schemas.achievement import AchievementCreate


def get_all_user_achievements(db: Session, current_user: user_model.User):
    return get_all_achievements(db, current_user.user_id)


def _is_achievement_exist(db: Session, user_id: int, achievement_name: str):
    all_achievements = get_all_achievements(db, user_id)
    achievement_list = [achievement.achievement_name for achievement in all_achievements]

    if achievement_name in achievement_list:
        return True

    return False


def create_achievement(db: Session, user_id: int, crate_datetime: datetime, achievement_name):
    new_achievement = AchievementCreate(achievement_name=achievement_name,
                                        achievement_date=crate_datetime)

    return create_achievement_in_db(db, user_id, new_achievement)


def check_achievements(db: Session, current_user: user_model.User):
    user_id = current_user.user_id
    achievements_count_before_check = get_achievement_count(db, user_id)
    current_datetime = datetime.now()

    comment_count = get_comment_count_for_user_id(db, user_id)
    post_count = get_post_count_for_user_id(db, user_id)
    measurement_count = get_measurement_count_for_user_id(db, user_id)

    for index in [1, 10, 25, 50, 100, 500]:
        comment_achievement_name = _get_comment_achievement_name(index)
        post_achievement_name = _get_post_achievement_name(index)
        measurement_achievement_name = _get_measure_achievement_name(index)

        if comment_count >= index:
            if not _is_achievement_exist(db, user_id, comment_achievement_name):
                create_achievement(db, user_id, current_datetime, comment_achievement_name)

        if post_count >= index:
            if not _is_achievement_exist(db, user_id, post_achievement_name):
                create_achievement(db, user_id, current_datetime, post_achievement_name)

        if measurement_count >= index:
            if not _is_achievement_exist(db, user_id, measurement_achievement_name):
                create_achievement(db, user_id, current_datetime, measurement_achievement_name)

    achievements_count_after_check = get_achievement_count(db, user_id)

    if achievements_count_after_check > achievements_count_before_check:
        return NEW_ACHIEVEMENTS_MESSAGE

    return NO_NEW_ACHIEVEMENTS_MESSAGE


def _get_comment_achievement_name(count):
    return f'Commentator! You write {count} comments!'


def _get_post_achievement_name(count):
    return f'Post Creator! You write {count} posts!'


def _get_measure_achievement_name(count):
    return f'Measure Master! You make {count} body measurements!'
