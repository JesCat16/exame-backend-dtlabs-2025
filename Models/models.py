from sqlalchemy import Column, Float, Integer, String
from DB.dbconnection import Base
from datetime import datetime

#Model for data receved, creation of database table
class IotData(Base):
    __tablename__ = 'dataIot'
    id = Column(Integer, primary_key=True, autoincrement= True)
    server_ulid = Column(String, index=True)
    timestamp = Column(String, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

#Model for servers, creation of database table
class Servershealth(Base):
    __tablename__ = 'serverHealth'
    server_ulid = Column(String, primary_key= True, index= True)
    status = Column(String, index= True)
    server_name = Column(String, index=True)

#Model for users, creation of database table
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement= True)
    user_name = Column(String, unique=True)
    password = Column(String)

