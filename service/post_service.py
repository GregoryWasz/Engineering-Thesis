from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from messages.messages import PERMISSION_ERROR, POST_NOT_EXIST_ERROR, POST_DELETE_MESSAGE, DATABASE_ERROR
from models import user_model
from repository.post_repository import (
    get_posts_from_db, create_post_in_db, get_single_post_by_post_id_from_db,
    delete_post_from_db,
)
from repository.user_repository import apply_changes_and_refresh_db
from schemas.post import PostCreate, PostNewTitle, PostNewText


# TODO this not make a sense loop?
def _raise_error_when_post_not_exist(post_id: int, db: Session):
    post = get_single_post_by_post_id_from_db(post_id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=POST_NOT_EXIST_ERROR,
        )

    return post


def _raise_error_when_user_is_not_post_owner(current_user_id: int, post_id: int, db: Session):
    post = _raise_error_when_post_not_exist(post_id, db)

    if current_user_id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=PERMISSION_ERROR,
        )


def get_posts(db: Session):
    return get_posts_from_db(db)


def create_single_post(post: PostCreate, db: Session, current_user: user_model.User):
    return create_post_in_db(post, db, current_user.user_id)


def get_single_post(post_id: int, db: Session):
    # TODO this not make a sense loop?
    _raise_error_when_post_not_exist(post_id, db)

    return get_single_post_by_post_id_from_db(post_id, db)


def delete_post_with_id(post_id: int, db: Session, current_user: user_model.User):
    _raise_error_when_user_is_not_post_owner(current_user.user_id, post_id, db)
    # TODO delete all comments which belongs to post
    if delete_post_from_db(post_id, db):
        return POST_DELETE_MESSAGE
    return DATABASE_ERROR


def update_post_title(post_id: int, post_title: PostNewTitle, db: Session, current_user: user_model.User):
    _raise_error_when_user_is_not_post_owner(current_user.user_id, post_id, db)

    post = get_single_post_by_post_id_from_db(post_id, db)
    post.post_title = post_title.post_title
    apply_changes_and_refresh_db(db, post)
    return post


def update_post_text(post_id: int, post_text: PostNewText, db: Session, current_user: user_model.User):
    _raise_error_when_user_is_not_post_owner(current_user.user_id, post_id, db)

    post = get_single_post_by_post_id_from_db(post_id, db)
    post.post_text = post_text.post_text
    apply_changes_and_refresh_db(db, post)
    return post
