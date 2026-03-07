from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session, InstrumentedAttribute

T = TypeVar("T")  # Tipo genérico para el modelo (Product, User, etc.)


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], db: Session):
        self.model = model    # Modelo SQLAlchemy (Product, User...)
        self.db = db          # Session inyectada

    # ===== CRUD BÁSICO =====
    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def get_by_id(self, entity_id: int) -> T | None:
        return (
            self.db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
        )

    def add(self, entity: T) -> T:
        self.db.add(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(entity)

    # Método para buscar por cualquier atributo
    def find_by_field(self, field: str, value) -> T | None:
        column: InstrumentedAttribute = getattr(self.model, field)

        return (
            self.db.query(self.model)
            .filter(column == value)
            .first()
        )

    # Método para buscar por cualquier atributo devolviendo list
    def find_all_by_field(self, field: str, value) -> list[T]:
        column: InstrumentedAttribute = getattr(self.model, field)

        return (
            self.db.query(self.model)
            .filter(column == value)
            .all()
        )

    # Método para buscar por igualdad entre atributo(repository.find_by(name="Laptop", stock=10)) devolviendo list
    def find_by(self, **filters) -> list[T]:
        query = self.db.query(self.model)

        for field, value in filters.items():
            column: InstrumentedAttribute = getattr(self.model, field)
            query = query.filter(column == value)

        return query.all()

    # Método para buscar por igualdad entre atributo(repository.find_by(name="Laptop", stock=10)) devolviendo optional
    def find_one_by(self, **filters) -> T | None:
        query = self.db.query(self.model)

        for field, value in filters.items():
            column: InstrumentedAttribute = getattr(self.model, field)
            query = query.filter(column == value)

        return query.first()

    # ===== PAGINACIÓN =====
    def get_paginated(self, page: int = 0, size: int = 10) -> list[T]:
        """
        page: índice empezando en 0 (como en Spring Data)
        size: tamaño de página
        """
        return (
            self.db.query(self.model)
            .offset(page * size)
            .limit(size)
            .all()
        )

    def count(self) -> int:
        """
        Total de registros (para calcular total_pages, etc.)
        """
        return self.db.query(self.model).count()
