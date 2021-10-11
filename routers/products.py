from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.dependencies import get_db, get_current_user
from models import user_model
from schemas.product import (
    ProductWithId, ProductCreate, ProductNewProductName, ProductNewProductDate,
    ProductNewProductCalorificValue,
)
from service import product_service

products = APIRouter()


@products.get("/", response_model=List[ProductWithId])
def get_all_products(current_user: user_model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return product_service.get_all_products(current_user, db)


@products.post("/", response_model=ProductWithId)
def create_products(product: ProductCreate, current_user: user_model.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    return product_service.create_product(product, current_user, db)


@products.get("/{id:path}", response_model=ProductWithId)
def get_product(id: int, current_user: user_model.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return product_service.get_single_product(id, current_user, db)


@products.delete("/{id:path}")
def delete_product(id: int, current_user: user_model.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return product_service.delete_single_product_by_id(id, current_user, db)


@products.put("/name/{id:path}", response_model=ProductWithId)
def update_product_name(id: int, product_name: ProductNewProductName,
                        current_user: user_model.User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return product_service.update_product_name(id, product_name, current_user, db)


@products.put("/date/{id:path}", response_model=ProductWithId)
def update_product_date(id: int, product_date: ProductNewProductDate,
                        current_user: user_model.User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return product_service.update_product_date(id, product_date, current_user, db)


@products.put("/calorific_value/{id:path}", response_model=ProductWithId)
def update_product_calorific_value(id: int, product_calorific_value: ProductNewProductCalorificValue,
                                   current_user: user_model.User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    return product_service.update_product_calorific_value(id, product_calorific_value, current_user, db)
