from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from clients.ai_clients import AIClient
from models.product import Product
from repositories.product_repository import ProductRepository
from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from service.ai_service import AIService


class ProductService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = ProductRepository(db)
        client = AIClient()
        self.ai_service = AIService(client)

    def create_product(self, product_create: ProductCreate) -> ProductResponse:
        # Validación del nombre
        existing_product = self.repository.find_by_exact_name(product_create.name)
        if existing_product is not None:
            raise HTTPException(
                status_code=400,
                detail="Product with this name already exists"
            )
        product = Product(**product_create.model_dump())

        # Creamos este try-except con IntegrityError para casos de concurrencia masiva,
        # la mayoría de veces no hace falta, pero como cuesta poco lo hacemos para prevenir
        try:
            self.repository.add(product)

            self.db.commit()

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Product with this name already exists"
            )
        self.db.refresh(product)

        return ProductResponse.model_validate(product)

    def get_product_by_id(self, id_product: int) -> ProductResponse:
        product = self.repository.get_by_id(id_product)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return ProductResponse.model_validate(product)

    def get_all_products(self) -> list[ProductResponse]:
        products = self.repository.get_all()

        return [ProductResponse.model_validate(p) for p in products]

    def update_product(self, id_product: int, product_update: ProductUpdate) -> ProductResponse:
        product = self.repository.get_by_id(id_product)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        # Más pyctonic
        # for field, value in product_update.model_dump(exclude_unset=True).items():
        #     setattr(product, field, value)
        # Más explícito, sirven ambas

        if product_update.name is not None:
            product.name = product_update.name

        if product_update.price is not None:
            product.price = product_update.price

        if product_update.stock is not None:
            product.stock = product_update.stock

        self.db.commit()
        self.db.refresh(product)

        return ProductResponse.model_validate(product)

    def delete_product(self, id_product: int) -> ProductResponse:
        product = self.repository.get_by_id(id_product)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        self.db.delete(product)
        self.db.commit()

        return ProductResponse.model_validate(product)

    # Calcular Stock para IA
    def _calculate_stock_status(self, stock: int) -> str:
        if stock == 0:
            return "out_of_stock"
        elif stock <= 5:
            return "low"
        elif stock <= 20:
            return "sufficient"
        else:
            return "high"

    async def analyze_product(self, product_id: int):

        product = self.repository.get_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        ai_result = await self.ai_service.analyze_product(
            product.name,
            product.price,
            product.stock
        )

        stock_status = self._calculate_stock_status(product.stock)

        return {
            **ai_result.model_dump(),
            "stock_status": stock_status
        }
