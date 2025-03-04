from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
import Models.models as models
from DB.dbconnection import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
import Security.auth as auth
import random
import string

app = FastAPI()
#Add router for authentication methods
app.include_router(auth.router)
#Create tables in DataBase
models.Base.metadata.create_all(bind = engine)

#Models for each methods
class Data(BaseModel):
    server_ulid: str
    timestamp: str
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

# Used to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Generate server_ulid
def id_generator(size=22, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Establish db_dependency
db_dependency = Annotated[Session, Depends(get_db)]
#Establish user_dependency
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

#Post data in DataBase 
@app.post("/data", status_code= auth.status.HTTP_200_OK)
async def postData(data: Data, db: db_dependency):
    db_data = models.IotData(server_ulid = data.server_ulid, timestamp = data.timestamp, temperature = data.temperature, 
                             humidity = data.humidity, voltage = data.voltage, current = data.current)
    db_server = db.query(models.Servershealth).filter(data.server_ulid == models.Servershealth.server_ulid).first()
    if db_server:
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    else:
        raise HTTPException(status_code=500)

#Get all data from DataBase
@app.get("/data")
async def Datas(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_datas = db.query(models.IotData).offset(0).limit(100).all()
    return db_datas

#Get data of a specific server from DataBase
@app.get("/data/{server_ulid}")
async def DatasServer(server_id: str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_datas = db.query(models.IotData).filter(server_id == models.IotData.server_ulid).order_by(models.IotData.id.desc()).first()
    return db_datas

#See all servers that were saved
@app.get("/health/all")
async def Servers(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_servers = db.query(models.Servershealth).offset(0).limit(100).all()
    return db_servers

#See health from one server
@app.get("/health/{server_id}",status_code= auth.status.HTTP_200_OK)
def healthServer(server_id: str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_server = db.query(models.Servershealth).filter(server_id == models.Servershealth.server_ulid).first()
    return db_server

#Save a server in DataBase
@app.post("/servers", status_code= auth.status.HTTP_200_OK)
async def postServers(server: ServerActivation, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    ulid = id_generator()
    db_server = models.Servershealth(server_ulid = ulid,status = 'offline',server_name = server.server_name)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

#Update servers status, can only be used by ServerStatus.py
@app.put("/updateServerStatus/{server_ulid}/{status}", include_in_schema=False)
def UpdateServerHealthStatus(server_ulid: str, status: str, db: db_dependency):
    db_server = db.query(models.Servershealth).filter(server_ulid == models.Servershealth.server_ulid).first()

    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    db_server.status = status
    db.commit()
    db.refresh(db_server)

#Get servers, used by workers
@app.get("/health", include_in_schema=False)
async def Servers(db: db_dependency):
    db_servers = db.query(models.Servershealth).offset(0).limit(100).all()
    return db_servers

#Get last data of a specific server, can only be used by ServerStatus.py 
@app.get("/dataIntern/{server_ulid}", include_in_schema=False)
def DatasIntern(server_ulid: str, db: db_dependency):
    db_datas = db.query(models.IotData).filter(server_ulid == models.IotData.server_ulid).order_by(models.IotData.id.desc()).first()
    return db_datas

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)