from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.configs.database.database import DBConfig

# Database setup
engine = create_engine(DBConfig.DB_URL, pool_pre_ping=True, echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
