from app.config import CONNECTION_STRING
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

raw_conn_str = os.getenv("SQL_CONNECTION_STRING")

params = urllib.parse.quote_plus(raw_conn_str)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()