from sqlalchemy import Column, Integer, String, Float
from .database import Base

class CarWork(Base):
    __tablename__ = "car_works"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True) 
    date = Column(String) 
    price = Column(Float)  
    file_path = Column(String, nullable=True)
