from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base
import models.user_model # noqa


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    product_date = Column(DateTime, index=True)
    product_calorific_value = Column(Float, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="products")
