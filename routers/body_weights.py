from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.body_weight_measure import (
    BodyWeightMeasure, BodyWeightMeasureWithId, BodyWeightMeasureCreate,
    BodyWeightMeasureNewWeight, BodyWeightMeasureNewDate,
)
from service.body_weight_service import (
    get_all_body_weights, get_single_body_weight, create_body_weight_measurement,
    delete_body_weight_measurement, update_body_measurement_weight_amount, update_body_measurement_date,
)

body_weight = APIRouter()


@body_weight.get("/", response_model=List[BodyWeightMeasureWithId])
def get_all_weights_measurements(db: Session = Depends(get_db),
                                 current_user: user_model.User = Depends(get_current_user)):
    return get_all_body_weights(db, current_user)


@body_weight.get("/{id:path}", response_model=BodyWeightMeasureWithId)
def get_single_weight_measurement(id: int, db: Session = Depends(get_db),
                                  current_user: user_model.User = Depends(get_current_user)):
    return get_single_body_weight(id, db, current_user)


@body_weight.post("/", response_model=BodyWeightMeasure)
def create_weight_measurement(body_weight_measure: BodyWeightMeasureCreate, db: Session = Depends(get_db),
                              current_user: user_model.User = Depends(get_current_user)):
    return create_body_weight_measurement(body_weight_measure, db, current_user)


@body_weight.delete("/{id:path}")
def delete_weight_measurement(id: int, db: Session = Depends(get_db),
                              current_user: user_model.User = Depends(get_current_user)):
    return delete_body_weight_measurement(id, db, current_user)


@body_weight.put("/weight/{id:path}", response_model=BodyWeightMeasure)
def update_weight_amount_for_weight_measurement(id: int, new_weight_amount: BodyWeightMeasureNewWeight,
                                                db: Session = Depends(get_db),
                                                current_user: user_model.User = Depends(get_current_user)):
    return update_body_measurement_weight_amount(id, new_weight_amount, db, current_user)


@body_weight.put("/date/{id:path}", response_model=BodyWeightMeasure)
def update_date_for_weight_measurement(id: int, new_date: BodyWeightMeasureNewDate, db: Session = Depends(get_db),
                                       current_user: user_model.User = Depends(get_current_user)):
    return update_body_measurement_date(id, new_date, db, current_user)
