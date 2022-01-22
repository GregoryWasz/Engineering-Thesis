from fastapi import HTTPException
from starlette import status

from messages.messages import CALORIE_TO_LOW_ERROR, TEXT_LENGTH_VALIDATION_ERROR


def _raise_http_exception(detail: str):
    """
    Zwróć błąd 409.

    :param detail: Tekst błędu
    :return: None
    """
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )


def _check_if_calorie_value_is_lower_than_0(calorie: int):
    """
    Zwróć błąd 500. Jeśli wartość kalorii jest mniejsza niż 0.

    :param calorie: Wartość kalorii
    :return: None
    """
    if calorie <= 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=CALORIE_TO_LOW_ERROR,
        )


def _validate_text_length(text: str):
    """
    Zwróć błąd jeśli długość tekstu jest mniejsza niż 3.

    :param text: Tekst do walidacji
    :return: None
    """
    if len(text) < 3:
        _raise_http_exception(TEXT_LENGTH_VALIDATION_ERROR)
