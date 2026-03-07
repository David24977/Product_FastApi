from fastapi import FastAPI
from core.db import Base, engine
from models import product  # IMPORTANTE: registrar modelo
from routers.product_router import router as product_router


def create_app() -> FastAPI:
    app = FastAPI(title="Product Microservice")
    # Para ver las tablas creadas, solo para información -> print("Tables registered in metadata:",
    # Base.metadata.tables.keys()) Crear tablas automáticamente
    Base.metadata.create_all(bind=engine)

    app.include_router(product_router)

    return app

