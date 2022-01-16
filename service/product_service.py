from sqlalchemy.orm import Session

from messages.messages import (
    PRODUCT_DELETE_MESSAGE, PRODUCT_DELETE_ERROR,
    PRODUCT_NAME_VALIDATION_ERROR,
)
from models import user_model
from repository.product_repository import (
    get_products_for_user_id, create_product_in_db, get_product_by_user_id,
    delete_product_by_id,
)
from repository.user_repository import apply_changes_and_refresh_db
from schemas.product import ProductCreate, ProductNewProductName, ProductNewProductDate, ProductNewProductCalorificValue


from service.user_service import _raise_http_exception


def get_all_products(current_user: user_model.User, db: Session):
    return get_products_for_user_id(current_user.user_id, db)


def create_product(product: ProductCreate, current_user: user_model.User, db: Session):
    product.product_date = product.product_date.replace(microsecond=0)

    _validate_product_name(product.product_name)
    # TODO validate calorie value > 0

    return create_product_in_db(product, current_user.user_id, db)


def get_single_product(id: int, current_user: user_model.User, db: Session):
    return get_product_by_user_id(id, current_user.user_id, db)


def delete_single_product_by_id(id: int, current_user: user_model.User, db: Session):
    if delete_product_by_id(id, current_user.user_id, db):
        return PRODUCT_DELETE_MESSAGE

    return PRODUCT_DELETE_ERROR


def update_product_name(id: int, product_name: ProductNewProductName, current_user: user_model.User, db: Session):
    # TODO check if product exist
    _validate_product_name(product_name.product_name)

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

    # TODO validate calorie value > 0
    product = get_product_by_user_id(id, current_user.user_id, db)
    product.product_calorific_value = product_calorific_value.product_calorific_value
    apply_changes_and_refresh_db(db, product)

    return product


def _validate_product_name(product_name):
    if len(product_name) < 4:
        _raise_http_exception(PRODUCT_NAME_VALIDATION_ERROR)
