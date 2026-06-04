from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Standard metadata naming convention for migration safety
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Declarative base
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))

def db_commit_safety(db: Session):
    """Safely commit a database session, rolling back on failure to ensure transaction safety."""
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
