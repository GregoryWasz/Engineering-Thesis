from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import models.post_model  # noqa
import models.user_model  # noqa
from db.database import Base


class Comment(Base):
    """
    Model dla bazy danych tworzący tabele Komentarze, wraz z odpowiednimi polami i relacjami.
    """
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    comment_text = Column(String, index=True)
    comment_date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    post_id = Column(Integer, ForeignKey("posts.post_id"))

    comment_creator = relationship("User", back_populates="comments")
    related_post = relationship("Post", back_populates="comments")
