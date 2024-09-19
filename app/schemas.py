from pydantic import BaseModel

class CarWorkCreate(BaseModel):
    description: str
    date: str
    price: float

class CarWork(BaseModel):
    id: int
    description: str
    date: str
    price: float

    class Config:
        from_attributes = True 
