from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Relationship, sessionmaker

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



Base.metadata.create_all(engine)