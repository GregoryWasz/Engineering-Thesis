from datetime import datetime

from pydantic import BaseModel

"""
Obiekty transferu danych dla modelu produktów.
"""


class Product(BaseModel):
    product_name: str
    product_date: datetime
    product_calorific_value: int

    class Config:
        orm_mode = True


class ProductWithId(Product):
    product_id: int


class ProductCreate(Product):
    pass


class ProductNewProductName(BaseModel):
    product_name: str

    class Config:
        orm_mode = True


class ProductNewProductDate(BaseModel):
    product_date: datetime

    class Config:
        orm_mode = True


class ProductNewProductCalorificValue(BaseModel):
    product_calorific_value: int

    class Config:
        orm_mode = True
