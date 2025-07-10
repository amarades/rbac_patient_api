from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------
# Database Configuration
# -----------------------------
DATABASE_URL = "postgresql://postgres:student@localhost:5432/postgres"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,            # Set to True if you want SQL logging for debugging
    future=True            # Use SQLAlchemy 2.0-style behavior
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

# Base class for models
Base = declarative_base()
