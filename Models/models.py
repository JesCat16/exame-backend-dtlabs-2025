from sqlalchemy import Column, ForeignKey, Float, Integer, String, DateTime, Boolean
from DB.dbconnection import Base
from datetime import datetime

class IotData(Base):
    __tablename__ = 'dataIot'
    id = Column(Integer, primary_key=True, autoincrement= True, index= True)
    server_ulid = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

class Servershealth(Base):
    __tablename__ = 'serverHealth'
    server_ulid = Column(String, primary_key= True, index= True)
    status = Column(Boolean, index= True)
    server_name = Column(String, index=True)

