from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship

class CarWork(Base):
    __tablename__ = "car_works"

    model_config = ConfigDict(from_attributes=True)
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True) 
    date = Column(String) 
    price = Column(Float)  
    file_path = Column(String, nullable=True)

    receipt_id = Column(Integer, ForeignKey('receipts.id'))
    receipt = relationship("Receipt", back_populates="car_works")


class Receipt(Base):
    __tablename__ = "receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    price = Column(String)
    date = Column(String)

    works = relationship("CarWork", back_populates="receipt")