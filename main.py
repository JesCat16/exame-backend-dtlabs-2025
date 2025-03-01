from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import Models.models as models
from DB.dbconnection import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class Data(BaseModel):
    server_ulid: str
    timestamp: datetime
    temperature: float
    humidity: float
    voltage: float
    current: float
    class Config:
        arbitrary_types_allowed = True

class ServersHealth(BaseModel):
    server_ulid: str
    status: str
    server_name: str

class ServerActivation(BaseModel):
    server_name: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.IotData).offset(skip).limit(limit).all()

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items

