from datetime import datetime

from sqlalchemy.orm import Session

from messages.messages import NO_NEW_ACHIEVEMENTS_MESSAGE, NEW_ACHIEVEMENTS_MESSAGE
from models import user_model
from repository.achievement_repository import get_all_achievements, get_achievement_count, create_achievement
from repository.body_weight_repository import get_measurement_count
from schemas.achievement import AchievementCreate


def get_all_user_achievements(db: Session, current_user: user_model.User):
    return get_all_achievements(db, current_user.user_id)


def _is_measurement_achievement_exist(db: Session, user_id: int, index: int):
    all_achievements = get_all_achievements(db, user_id)
    achievement_list = [achievement.achievement_name for achievement in all_achievements]

    if _get_measure_achievement_name(index) in achievement_list:
        return True

    return False


def create_measure_master_achievement(db: Session, user_id: int, index: int, crate_datetime: datetime):
    new_achievement = AchievementCreate(achievement_name=_get_measure_achievement_name(index),
                                        achievement_date=crate_datetime)

    return create_achievement(db, user_id, new_achievement)


def check_achievements(db: Session, current_user: user_model.User):
    user_id = current_user.user_id
    achievements_count_before_check = get_achievement_count(db, user_id)
    current_datetime = datetime.now()

    # comment_count = _get_comment_count()
    # post_count = _get_post_count()
    measurement_count = get_measurement_count(db, user_id)

    for index in [1, 10, 25, 50, 100, 500]:
        # if comment_count > index:
        #     if not _is_comment_exist():
        #         create_commentator_achievement()
        #
        # if post_count > index:
        #     if not _is_post_exist():
        #         create_post_creator_achievement()

        if measurement_count >= index:
            if not _is_measurement_achievement_exist(db, user_id, index):
                create_measure_master_achievement(db, user_id, index, current_datetime)

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
