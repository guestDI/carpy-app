from sqlalchemy import Column, Integer, String, Float
from .database import Base
from pydantic import BaseModel, ConfigDict

class CarWork(Base):
    __tablename__ = "car_works"
    model_config = ConfigDict(from_attributes=True)
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True) 
    date = Column(String) 
    price = Column(Float)  
    file_path = Column(String, nullable=True)
