from typing import List
from pydantic import BaseModel

class WorkBase(BaseModel):
    description: str
    date: str
    price: float

class CarWorkCreate(WorkBase):
    pass

class CarWork(WorkBase):
    id: int
    receipt_id: int

    class Config:
        from_attributes = True 


#split on different file
class ReceiptBase(BaseModel):
    content: str
    price: str
    date: str

class ReceiptCreate(ReceiptBase):
    works: List[CarWorkCreate] = []

class Receipt(ReceiptBase):
    id: int
    works: List[CarWork] = []

    class Config:
        from_attributes = True