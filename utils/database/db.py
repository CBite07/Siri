from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://siri_db_manager:siri_db_manager@localhost:3306/siri_db?charset=utf8mb4"

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    echo=True
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()