from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from psycopg2 import *

URL_DATABASE = "postgresql://postgres:juju0101@localhost:5432/postgres"

engine = create_engine(URL_DATABASE, echo=True)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()
