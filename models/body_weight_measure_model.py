from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base
import models.user_model # noqa


class BodyWeightMeasure(Base):
    __tablename__ = "body_weight_measurements"

    body_weight_measure_id = Column(Integer, primary_key=True, index=True)
    weight_amount = Column(Float, index=True)
    weighting_date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="body_weight_measurements")
