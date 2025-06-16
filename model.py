# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    house_number = Column(String, index=True)
    month_year = Column(String, index=True)
    image_filename = Column(String)
    amount_verified = Column(Boolean)
    upload_time = Column(DateTime, default=datetime.utcnow)
