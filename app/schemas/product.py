from decimal import Decimal

from pydantic import BaseModel, Field


# Base común en ambos dtos
class ProductBase(BaseModel):
    name: str = Field(..., max_length=50)
    price: Decimal = Field(..., ge=0)  # ge = mayor o igual al número que pongas
    stock: int = Field(..., ge=0)


# Para crear(RequestDto)
class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None


# Para devolver(ResponseDto)
class ProductResponse(ProductBase):
    id: int

    # Convertir automáticamente un objeto SQLAlchemy en schema(MapStruck)
    class Config:
        from_attributes = True
