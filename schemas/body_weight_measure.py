from datetime import datetime

from pydantic import BaseModel


class BodyWeightMeasure(BaseModel):
    body_weight_measure_id: int
    weight_amount: str
    weighting_date: datetime
    # user_id: int
