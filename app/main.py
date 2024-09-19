import shutil
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app import models, schemas, database, receipt_processor
from pathlib import Path
from .database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True) 

models.Base.metadata.create_all(bind=database.engine)

@app.get("/car-works/", response_model=list[schemas.CarWork])
def get_car_works(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    car_works = db.query(schemas.CarWork).offset(skip).limit(limit).all()
    return car_works

@app.get("/car-works/search/")
def search_car_works(
    start_date: str = None, 
    end_date: str = None, 
    min_price: float = None, 
    max_price: float = None, 
    db: Session = Depends(database.get_db)
):
    query = db.query(models.CarWork)
    if start_date and end_date:
        query = query.filter(models.CarWork.date.between(start_date, end_date))
    if min_price:
        query = query.filter(models.CarWork.price >= min_price)
    if max_price:
        query = query.filter(models.CarWork.price <= max_price)
    return query.all()


@app.post("/car-works/", response_model=schemas.CarWork)
def create_car_work(car_work: schemas.CarWorkCreate, db: Session = Depends(database.get_db)):
    db_car_work = schemas.CarWork(**car_work.dict())
    db.add(db_car_work)
    db.commit()
    db.refresh(db_car_work)
    return db_car_work

@app.post("/car-works/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": str(file_path)}

# Если необходимо связать с записью о работе
@app.post("/car-works/{car_work_id}/upload/")
async def upload_file_for_work(car_work_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    car_work = db.query(models.CarWork).filter(models.CarWork.id == car_work_id).first()
    if not car_work:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Сохраняем путь к файлу в базе данных (при необходимости)
    car_work.file_path = str(file_path)
    db.commit()

    return {"filename": file.filename, "path": str(file_path)}

@app.get("/car-works/stats/")
def get_stats(month: int, year: int, db: Session = Depends(database.get_db)):
    total_expense = db.query(func.sum(models.CarWork.price)).filter(
        extract('month', models.CarWork.date) == month,
        extract('year', models.CarWork.date) == year
    ).scalar()

    return {"total_expense": total_expense or 0}

@app.post("/upload-receipt/", response_model=schemas.Receipt)
async def upload_receipt(
    file: UploadFile = File(...),
    works: list[schemas.WorkCreate] = [],
    db: Session = Depends(get_db)
):
    file_path = f"./{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    receipt_data = receipt_processor.process_receipt_image(file_path)
    
    receipt_db = models.Receipt(
        content=receipt_data["content"],
        price=receipt_data["price"],
        date=receipt_data["date"]
    )
    db.add(receipt_db)
    db.commit()
    db.refresh(receipt_db)

    for work in works:
        work_db = models.Work(**work.dict(), receipt_id=receipt_db.id)
        db.add(work_db)
    
    db.commit()

    return receipt_db