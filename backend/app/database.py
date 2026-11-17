
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Database connection URL
DATABASE_URL = "sqlite:///./resumeiq.db"


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Create database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# Base class for all database models
class Base(DeclarativeBase):
    pass


# Import models after Base is defined
from app.models import user, resume


# Database dependency for FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create database tables
def create_tables():
    Base.metadata.create_all(bind=engine)
