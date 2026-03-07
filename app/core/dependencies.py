from fastapi import Depends
from sqlalchemy.orm import Session

from core.db import get_db
from service.product_service import ProductService


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)
