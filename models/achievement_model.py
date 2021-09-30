from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base
import models.user_model # noqa


class Achievement(Base):
    __tablename__ = "achievements"

    achievement_id = Column(Integer, primary_key=True, index=True)
    achievement_name = Column(String, index=True)
    achievement_date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="achievements")
