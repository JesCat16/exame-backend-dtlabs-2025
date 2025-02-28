from sqlalchemy import Column, ForeignKey, Float, Integer, String, DateTime, Boolean
from Classes.servers import ServersHealth
from dbconnection import Base

class IotData(Base):
    __tablename__ = 'DataIot'
    id = Column(Integer, primary_key=True, autoincrement= True, index= True)
    server_ulid = Column(String, index=True)
    timestamp = Column(DateTime, index= True)
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

class Servers(Base):
    __tablename__: 'ServerHealth'
    server_ulid = Column(String, primary_key= True, index= True)
    status = Column(Boolean, index= True)
    server_name = Column(String, index=True)
