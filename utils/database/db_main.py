from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from utils.configs.database.database import DBConfig

engine = create_engine(DBConfig.DB_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    db_session = SessionLocal()
    try:
        yield db_session
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise
    except Exception:
        raise
    finally:
        db_session.close()
