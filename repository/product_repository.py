from datetime import date

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import product_model
from schemas.product import ProductCreate


def get_products_for_user_id(user_id: int, db: Session):
    return db.query(product_model.Product).filter(product_model.Product.user_id == user_id).all()


def get_products_for_user_id_with_date(current_date: date, user_id: int, db: Session):
    return db.query(product_model.Product).filter(product_model.Product.user_id == user_id,
                                                  func.DATE(product_model.Product.product_date) == current_date).all()


def create_product_in_db(product: ProductCreate, user_id: int, db: Session):
    """
    Tworzenie produktu w bazie danych.

    :param product: Obiekt produktu
    :param db: Sesja bazy danych
    :param user_id: Identyfikator użytkownika
    :return: Produkt
    """
    db_product = product_model.Product(user_id=user_id, **product.__dict__)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_user_id(product_id: int, user_id: int, db: Session):
    return db.query(product_model.Product).filter(product_model.Product.user_id == user_id,
                                                  product_model.Product.product_id == product_id).first()


def delete_product_by_id(product_id: int, user_id: int, db: Session):
    """
    Usuwanie z bazy danych produktu.

    :param db: Sesja bazy danych
    :param product_id: Identyfikator produktu
    :param user_id: Identyfikator użytkownika
    :return: Wartość boolowska Prawda/Fałsz
    """
    try:
        product = get_product_by_user_id(product_id, user_id, db)
        db.delete(product)
        db.commit()
    except SQLAlchemyError:
        return False
    return True
