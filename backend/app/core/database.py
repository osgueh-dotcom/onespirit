from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

def db_commit_safety(db: Session):
    """Safely commit a database session, rolling back on failure to ensure transaction safety."""
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
