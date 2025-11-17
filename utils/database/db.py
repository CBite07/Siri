from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.configs.database.database import DBConfig

engine = create_engine(DBConfig.DB_URL, pool_pre_ping=True, echo=False)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
