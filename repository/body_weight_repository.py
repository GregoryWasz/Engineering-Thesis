from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import body_weight_measure_model
from schemas.body_weight_measure import BodyWeightMeasureCreate


def get_body_weight_measurements(db: Session, user_id: int):
    """
    Pobieranie z bazy danych pomiary masy ciała dla danego użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Lista pomiarów masy ciała użytkownika
    """
    return db.query(body_weight_measure_model.BodyWeightMeasure).filter(
        body_weight_measure_model.BodyWeightMeasure.user_id == user_id).all()


def get_body_weight_measurement(db: Session, user_id: int, body_weight_id: int):
    """
    Pobieranie z bazy danych pomiar masy ciała o wskazanym identyfikatorze.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :param body_weight_id: Identyfikator pomiaru masy ciała użytkownika
    :return: Pomiar masy ciała użytkownika
    """
    return db.query(body_weight_measure_model.BodyWeightMeasure).filter(
        body_weight_measure_model.BodyWeightMeasure.user_id == user_id,
        body_weight_measure_model.BodyWeightMeasure.body_weight_measure_id == body_weight_id,
    ).first()


def create_body_weight_measurement_in_db(db: Session, user_id: int, body_weight: BodyWeightMeasureCreate):
    """
    Tworzenie w bazie danych nowego pomiaru masy ciała użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :param body_weight: Obiekt tworzenia pomiaru masy ciała użytkownika
    :return: Pomiar masy ciała użytkownika
    """
    db_body_weight_measure = body_weight_measure_model.BodyWeightMeasure(user_id=user_id, **body_weight.__dict__)
    db.add(db_body_weight_measure)
    db.commit()
    db.refresh(db_body_weight_measure)
    return db_body_weight_measure


def delete_body_weight_measurement_from_db(db: Session, user_id: int, body_weight_id: int):
    """
    Usuwanie z bazy danych pomiaru masy ciała użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :param body_weight_id: Identyfikator pomiaru masy ciała użytkownika
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        current_body_measurement = get_body_weight_measurement(db, user_id, body_weight_id)
        db.delete(current_body_measurement)
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def get_measurement_count_for_user_id(db: Session, user_id: int):
    """
    Pobieranie z bazy danych liczby pomiarów masy ciała dla danego użytkownika.

    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Liczba całkowita
    """
    return db.query(body_weight_measure_model.BodyWeightMeasure).filter(
        body_weight_measure_model.BodyWeightMeasure.user_id == user_id).count()
