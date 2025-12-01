from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()




class HourlyStats(Base):
    __tablename__ = "hourly_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hour = Column(Integer)  # 0-23 soat
    joined_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String)  # unique bo‘lmaydi, har kirish alohida yoziladi
    full_name = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)
    left_at = Column(DateTime, nullable=True)
    duration_in_group = Column(Integer, nullable=True)  # sekundda