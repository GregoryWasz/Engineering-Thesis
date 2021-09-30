from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    product_name: str
    product_date: datetime
    product_calorific_value: float
    # user_id: int
