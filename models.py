from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import Relationship, sessionmaker
from datetime import datetime


Base = declarative_base()



username = "postgres"
password = "postgres"
host = "127.0.0.1"
port = 5432
db_name = "bookdb"

DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
engine = create_engine(DATABASE_URL)


Session = sessionmaker(bind=engine)
session = Session()


class TimeStampModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow(), nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow(), nullable=True)

from bookapp.models import *
from userapp.models import *

Base.metadata.create_all(engine)