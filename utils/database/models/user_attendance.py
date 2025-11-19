from sqlalchemy import Column, BigInteger, Date, Integer
from ..db import Base


class UserAttendance(Base):
    __tablename__ = "user_attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(BigInteger, primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    streak = Column(Integer, default=0)
