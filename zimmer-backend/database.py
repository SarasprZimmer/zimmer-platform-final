import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

load_dotenv()

# Naming convention for constraints
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

# Get DATABASE_URL from environment, fallback to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
if DATABASE_URL is None or DATABASE_URL.strip() == "":
    DATABASE_URL = "sqlite:///./dev.db"
    print("⚠️  No DATABASE_URL found in .env, using SQLite for development")

# Configure engine with optimized connection pooling
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration - optimized for performance
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30,  # 30 second timeout
            "isolation_level": None  # Autocommit mode for better performance
        },
        poolclass=QueuePool,
        pool_size=5,  # Reduced pool size for SQLite
        max_overflow=10,  # Reduced overflow
        pool_pre_ping=True,
        pool_recycle=1800,  # 30 minutes recycle
        future=True,
        echo=False,
        # SQLite-specific optimizations
        pool_timeout=30,
        pool_reset_on_return='commit'
    )
else:
    # PostgreSQL configuration - optimized for performance
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,  # Reduced pool size
        max_overflow=10,  # Reduced overflow
        pool_pre_ping=True,
        pool_recycle=1800,  # 30 minutes recycle
        future=True,
        echo=False,
        pool_timeout=30,
        pool_reset_on_return='commit'
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 