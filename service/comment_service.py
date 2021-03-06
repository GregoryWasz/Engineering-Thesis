from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from messages.messages import PERMISSION_ERROR, COMMENT_NOT_EXIST_ERROR, COMMENT_DELETE_MESSAGE, DATABASE_ERROR
from models import user_model
from repository.comment_repository import (
    create_comment_in_db, get_single_comment_by_comment_id_from_db,
    delete_comment_from_db, get_comments_by_post_id_from_db,
)
from repository.common_database_functions import apply_changes_and_refresh_db
from schemas.comment import (
    CommentCreate, CommentNewText,
)
from service.post_service import _raise_error_when_post_not_exist
from service.common_error_functions import _validate_text_length


def _when_comment_not_exist_raise_error(comment):
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=COMMENT_NOT_EXIST_ERROR,
        )


def _get_and_validate_comment(comment_id: int, db: Session):
    comment = get_single_comment_by_comment_id_from_db(comment_id, db)
    _when_comment_not_exist_raise_error(comment)
    return comment


def _raise_error_when_user_is_not_comment_owner(current_user_id: int, comment_id: int, db: Session):
    comment = _get_and_validate_comment(comment_id, db)

    if current_user_id != comment.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=PERMISSION_ERROR,
        )


def create_single_comment(post_id: int, comment: CommentCreate, db: Session, current_user: user_model.User):
    _raise_error_when_post_not_exist(post_id, db)
    _validate_text_length(comment.comment_text)

    return create_comment_in_db(post_id, comment, db, current_user.user_id)


def get_comments_for_post(post_id: int, db: Session):
    return get_comments_by_post_id_from_db(post_id, db)


def delete_comment_with_id(comment_id: int, db: Session, current_user: user_model.User):
    _raise_error_when_user_is_not_comment_owner(current_user.user_id, comment_id, db)

    if delete_comment_from_db(comment_id, db):
        return COMMENT_DELETE_MESSAGE
    return DATABASE_ERROR


def update_comment_text(comment_id: int, new_comment_text: CommentNewText, db: Session, current_user: user_model.User):
    _raise_error_when_user_is_not_comment_owner(current_user.user_id, comment_id, db)
    _validate_text_length(new_comment_text.comment_text)

    comment = get_single_comment_by_comment_id_from_db(comment_id, db)
    comment.comment_text = new_comment_text.comment_text
    apply_changes_and_refresh_db(db, comment)
    return comment
