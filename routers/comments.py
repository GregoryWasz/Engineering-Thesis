from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.comment import (
    CommentResp, CommentCreate, CommentNewText,
)
from service.comment_service import (
    create_single_comment, get_single_comment, delete_comment_with_id, update_comment_text,
)

comments = APIRouter()


@comments.post("/{post_id:path}", response_model=CommentResp)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db),
                   current_user: user_model.User = Depends(get_current_user)):
    return create_single_comment(post_id, comment, db, current_user)


@comments.get("/{comment_id:path}", response_model=CommentResp)
def get_comment_with_id(comment_id: int, db: Session = Depends(get_db)):
    return get_single_comment(comment_id, db)


@comments.delete("/{comment_id:path}")
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                   current_user: user_model.User = Depends(get_current_user)):
    return delete_comment_with_id(comment_id, db, current_user)


@comments.put("/text/{comment_id:path}", response_model=CommentResp)
def change_comment_text(comment_id: int, new_comment_text: CommentNewText, db: Session = Depends(get_db),
                        current_user: user_model.User = Depends(get_current_user)):
    return update_comment_text(comment_id, new_comment_text, db, current_user)
