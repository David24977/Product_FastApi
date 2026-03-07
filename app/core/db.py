from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.core.config import settings


# 1️.Construimos la URL de conexión
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)


# 2️.Creamos el engine (equivalente a DataSource)
engine = create_engine(
    DATABASE_URL,
    echo=True  # pon True si quieres ver el SQL en consola
)


# 3️.Creamos la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)


# 4️.Base para los modelos (equivalente a @Entity)
class Base(DeclarativeBase):
    pass


# 5️.Dependencia para inyectar DB en los servicios
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
