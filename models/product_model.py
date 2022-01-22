from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import models.user_model  # noqa
from db.database import Base


class Product(Base):
    """
    Model dla bazy danych tworzący tabele Produkty, wraz z odpowiednimi polami i relacjami.
    """
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    product_date = Column(DateTime, index=True)
    product_calorific_value = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="products")
