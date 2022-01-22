from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import models.user_model  # noqa
from db.database import Base


class Achievement(Base):
    """
    Model dla bazy danych tworzący tabele Osiągnięcia, wraz z odpowiednimi polami i relacjami.
    """
    __tablename__ = "achievements"

    achievement_id = Column(Integer, primary_key=True, index=True)
    achievement_name = Column(String, index=True)
    achievement_date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="achievements")
