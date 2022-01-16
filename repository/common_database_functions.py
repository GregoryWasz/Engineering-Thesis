from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def apply_changes_in_db(db: Session):
    try:
        db.commit()
    except SQLAlchemyError:
        return False
    return True


def apply_changes_and_refresh_db(db: Session, instance: Any):
    apply_changes_in_db(db)
    db.refresh(instance)