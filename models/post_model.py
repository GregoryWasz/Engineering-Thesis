from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base
import models.comment_model # noqa
import models.user_model # noqa


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    post_title = Column(String, index=True)
    post_text = Column(String, index=True)
    post_date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    post_creator = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="related_post")
