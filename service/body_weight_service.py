from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from messages.messages import BODY_MEASUREMENT_DELETE_MESSAGE, BODY_MEASUREMENT_DELETE_ERROR
from models import user_model
from repository.body_weight_repository import (
    get_body_weight_measurements, get_body_weight_measurement,
    create_body_weight_measurement_in_db, delete_body_weight_measurement_from_db,
)
from repository.user_repository import apply_changes_and_refresh_db
from schemas.body_weight_measure import BodyWeightMeasureCreate, BodyWeightMeasureNewWeight, BodyWeightMeasureNewDate


def get_all_body_weights(db: Session, current_user: user_model.User):
    return get_body_weight_measurements(db, current_user.user_id)


def get_single_body_weight(body_weight_id: int, db: Session, current_user: user_model.User):
    return get_body_weight_measurement(db, current_user.user_id, body_weight_id)


def create_body_weight_measurement(body_weight_measure: BodyWeightMeasureCreate, db: Session,
                                   current_user: user_model.User):
    # TODO validate BW > 0
    return create_body_weight_measurement_in_db(db, current_user.user_id, body_weight_measure)


def delete_body_weight_measurement(body_weight_id: int, db: Session, current_user: user_model.User):
    _check_if_body_measurement_exist(body_weight_id, db, current_user)

    if delete_body_weight_measurement_from_db(db, current_user.user_id, body_weight_id):
        return BODY_MEASUREMENT_DELETE_MESSAGE


def update_body_measurement_weight_amount(body_weight_id: int, new_weight_amount: BodyWeightMeasureNewWeight,
                                          db: Session, current_user: user_model.User):
    _check_if_body_measurement_exist(body_weight_id, db, current_user)

    # TODO validate BW > 0
    body_measurement = get_body_weight_measurement(db, current_user.user_id, body_weight_id)
    body_measurement.weight_amount = new_weight_amount.weight_amount
    apply_changes_and_refresh_db(db, body_measurement)

    return body_measurement


def update_body_measurement_date(body_weight_id: int, new_date: BodyWeightMeasureNewDate, db: Session,
                                 current_user: user_model.User):
    _check_if_body_measurement_exist(body_weight_id, db, current_user)

    body_measurement = get_body_weight_measurement(db, current_user.user_id, body_weight_id)
    body_measurement.weighting_date = new_date.weighting_date
    apply_changes_and_refresh_db(db, body_measurement)
    return body_measurement


def _check_if_body_measurement_exist(body_weight_id: int, db: Session, current_user: user_model.User):
    if not get_body_weight_measurement(db, current_user.user_id, body_weight_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=BODY_MEASUREMENT_DELETE_ERROR,
        )
