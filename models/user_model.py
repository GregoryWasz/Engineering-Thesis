from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

import models.achievement_model  # noqa
import models.body_weight_measure_model  # noqa
import models.comment_model  # noqa
import models.post_model  # noqa
import models.product_model  # noqa
from db.database import Base


class User(Base):
    """
    Model dla bazy danych tworzący tabele Użytkownicy, wraz z odpowiednimi polami i relacjami.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    calorie_limit = Column(Integer)

    achievements = relationship("Achievement", back_populates="owner")
    products = relationship("Product", back_populates="owner")
    posts = relationship("Post", back_populates="post_creator")
    comments = relationship("Comment", back_populates="comment_creator")
    body_weight_measurements = relationship("BodyWeightMeasure", back_populates="owner")
