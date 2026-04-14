from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase


from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()


url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("db_user"),
    password=os.getenv("db_password"),
    host=os.getenv("db_host"),
    database=os.getenv("db_name"),
    port=int(os.getenv("db_port", 5432))
)


# Create the SQLAlchemy engine
engine = create_engine(url)
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
# engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

import app.models

def get_db():#Crea sesiones en el database
    db = SessionLocal()
    try:
        print("Conexión abierta")
        yield db
    finally:
        db.close()
        print("Conexión cerrada")


