from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import Models.models as models
from DB.dbconnection import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime
import Security.auth as auth
import random
import string

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

def id_generator(size=22, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.get("/health")
async def Servers(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_servers = db.query(models.Servershealth).offset(0).limit(100).all()
    return db_servers

@app.get("/health/{server_id}",status_code= auth.status.HTTP_200_OK)
def healthServer(server_id: str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_server = db.query(models.Servershealth).filter(server_id == models.Servershealth.server_ulid).first()
    return db_server

@app.post("/servers", status_code= auth.status.HTTP_200_OK)
async def postServers(server: ServerActivation, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    ulid = id_generator()
    db_server = models.Servershealth(server_ulid = ulid,status = 'offline',server_name = server.server_name)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return server


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)