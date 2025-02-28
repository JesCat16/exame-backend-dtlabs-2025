from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import models
from dbconnection import engine, SessionLocal
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
