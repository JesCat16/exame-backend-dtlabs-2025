from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import Models.models as models
from DB.dbconnection import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime
import auth

app = FastAPI()
app.include_router(auth.router)
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
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

# @app.get("/data")
# async def readData():

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)