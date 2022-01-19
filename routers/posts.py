from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.post import (
    PostResp, PostCreate, PostNewText, PostNewTitle,
)
from service.post_service import (
    get_posts, get_single_post, create_single_post, delete_post_with_id, update_post_title,
    update_post_text,
)

posts = APIRouter()


@posts.get("", response_model=List[PostResp])
def get_all_posts(db: Session = Depends(get_db)):
    return get_posts(db)


@posts.post("", response_model=PostResp)
def create_post(post: PostCreate, db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    return create_single_post(post, db, current_user)


@posts.get("/{post_id:path}", response_model=PostResp)
def get_post_with_id(post_id: int, db: Session = Depends(get_db)):
    return get_single_post(post_id, db)


@posts.delete("/{post_id:path}")
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    return delete_post_with_id(post_id, db, current_user)


@posts.put("/title/{post_id:path}", response_model=PostResp)
def change_post_title(post_id: int, post_title: PostNewTitle, db: Session = Depends(get_db),
                      current_user: user_model.User = Depends(get_current_user)):
    return update_post_title(post_id, post_title, db, current_user)


@posts.put("/text/{post_id:path}", response_model=PostResp)
def change_post_text(post_id: int, post_text: PostNewText, db: Session = Depends(get_db),
                     current_user: user_model.User = Depends(get_current_user)):
    return update_post_text(post_id, post_text, db, current_user)
