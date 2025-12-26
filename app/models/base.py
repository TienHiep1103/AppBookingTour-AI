from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    LargeBinary
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id = Column("Id", Integer, primary_key=True, index=True)

    created_at = Column( "CreatedAt", DateTime, nullable=False, server_default=func.now())
    updated_at = Column( "UpdatedAt", DateTime, nullable=True, onupdate=func.now())

    # Concurrency token (rowversion / timestamp)
    row_version = Column( "RowVersion", LargeBinary, nullable=False)