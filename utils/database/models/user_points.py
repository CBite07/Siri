from sqlalchemy import Column, BigInteger, Integer, DateTime, text
from sqlalchemy.sql import func
from ..db import Base


class UserPoints(Base):
    __tablename__ = "user_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(BigInteger, unique=True, nullable=False)
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
