from datetime import datetime

from pydantic import BaseModel


class BodyWeightMeasure(BaseModel):
    weight_amount: float
    weighting_date: datetime

    class Config:
        orm_mode = True


class BodyWeightMeasureCreate(BodyWeightMeasure):
    pass


class BodyWeightMeasureWithId(BodyWeightMeasure):
    body_weight_measure_id: int


class BodyWeightMeasureNewWeight(BaseModel):
    weight_amount: int

    class Config:
        orm_mode = True


class BodyWeightMeasureNewDate(BaseModel):
    weighting_date: datetime

    class Config:
        orm_mode = True
