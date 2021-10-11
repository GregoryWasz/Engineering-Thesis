from sqlalchemy.orm import Session

from messages.messages import PRODUCT_DELETE_MESSAGE, PRODUCT_DELETE_ERROR
from models import user_model
from repository.product_repository import (
    get_products_for_user_id, create_product_in_db, get_product_by_user_id,
    delete_product_by_id,
)
from repository.user_repository import apply_changes_and_refresh_db
from schemas.product import ProductCreate, ProductNewProductName, ProductNewProductDate, ProductNewProductCalorificValue


# TODO Handle errors
# TODO Add tests


def get_all_products(current_user: user_model.User, db: Session):
    return get_products_for_user_id(current_user.user_id, db)


def create_product(product: ProductCreate, current_user: user_model.User, db: Session):
    # TODO Validate inputs
    return create_product_in_db(product, current_user.user_id, db)


def get_single_product(id: int, current_user: user_model.User, db: Session):
    return get_product_by_user_id(id, current_user.user_id, db)


def delete_single_product_by_id(id: int, current_user: user_model.User, db: Session):
    if delete_product_by_id(id, current_user.user_id, db):
        return PRODUCT_DELETE_MESSAGE

    return PRODUCT_DELETE_ERROR


def update_product_name(id: int, product_name: ProductNewProductName, current_user: user_model.User, db: Session):
    # TODO check if product exist
    product = get_product_by_user_id(id, current_user.user_id, db)
    product.product_name = product_name.product_name
    apply_changes_and_refresh_db(db, product)

    return product


def update_product_date(id: int, product_date: ProductNewProductDate, current_user: user_model.User, db: Session):
    # TODO check if product exist
    product = get_product_by_user_id(id, current_user.user_id, db)
    product.product_date = product_date.product_date
    apply_changes_and_refresh_db(db, product)

    return product


def update_product_calorific_value(id: int, product_calorific_value: ProductNewProductCalorificValue,
                                   current_user: user_model.User, db: Session):

    # TODO check if product exist
    product = get_product_by_user_id(id, current_user.user_id, db)
    product.product_calorific_value = product_calorific_value.product_calorific_value
    apply_changes_and_refresh_db(db, product)

    return product
