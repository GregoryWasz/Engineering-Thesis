from fastapi import HTTPException
from starlette import status

from messages.messages import CALORIE_TO_LOW_ERROR, TEXT_LENGTH_VALIDATION_ERROR


def _raise_http_exception(detail):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )


def _check_if_calorie_value_is_lower_than_0(calorie: int):
    if calorie <= 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=CALORIE_TO_LOW_ERROR,
        )


def _validate_text_length(text):
    if len(text) < 3:
        _raise_http_exception(TEXT_LENGTH_VALIDATION_ERROR)