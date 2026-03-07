from sqlalchemy.orm import Session
from models.product import Product
from repositories.base_repository import BaseRepository
from typing import cast, List


class ProductRepository(BaseRepository[Product]):

    def __init__(self, db: Session):
        super().__init__(Product, db)

    # Aquí podemos añadir métodos específicos de Product
    # por ejemplo:
    def find_by_name(self, name: str) -> list[Product]:
        return cast(
            List[Product],
            self.db.query(self.model)
            .filter(self.model.name.ilike(f"%{name}%"))
            .all()
        )

    def find_by_exact_name(self, name: str) -> Product | None:
        return (
            self.db.query(Product)
            .filter(Product.name == name)
            .first()
        )
