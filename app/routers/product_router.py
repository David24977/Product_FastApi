from fastapi import APIRouter, Depends

from core.dependencies import get_product_service
from schemas.product import ProductResponse, ProductCreate, ProductUpdate
from schemas.product_ai import ProductAIAnalysisFullResponse
from service.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("", response_model=ProductResponse)
def created_product(product_create: ProductCreate,
                    service: ProductService = Depends(get_product_service)):
    return service.create_product(product_create)


@router.get("/{id_product}", response_model=ProductResponse)
def get_product_by_id(
        id_product: int,
        service: ProductService = Depends(get_product_service)):
    return service.get_product_by_id(id_product)


@router.get("", response_model=list[ProductResponse])
def get_all_products(
        service: ProductService = Depends(get_product_service)
):
    return service.get_all_products()


@router.patch("/{id_product}", response_model=ProductResponse)
def update_product(
        id_product: int,
        product_update: ProductUpdate,
        service: ProductService = Depends(get_product_service)
):
    return service.update_product(id_product, product_update)


@router.delete("/{id_product}", response_model=ProductResponse)
def delete_product(
        id_product: int,
        service: ProductService = Depends(get_product_service)
):
    return service.delete_product(id_product)


@router.post("/{product_id}/ai/analyze", response_model=ProductAIAnalysisFullResponse)
async def analyze_product(product_id: int,
                          service: ProductService = Depends(get_product_service)):
    return await service.analyze_product(product_id)
