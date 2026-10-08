from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from config import DB_SERVER, DB_NAME

connection_url = URL.create(
    "mssql+pyodbc",
    host=DB_SERVER,
    database=DB_NAME,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "trusted_connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(connection_url)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()