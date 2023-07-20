from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        create_engine, inspect)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship, sessionmaker

# from alembic import sqlalchemy_url

Base = declarative_base()

username = "postgres"
password = "postgres"
host = "127.0.0.1"
port = 5432
db_name = "bookdb"


engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')


# inspector = inspect(engine)

# # Get a list of table names in the database
# table_names = inspector.get_table_names()

# # Print the table names
# print("Table names in the database:")
# for table_name in table_names:
#     print(table_name)


Session = sessionmaker(bind=engine)
session = Session()


class TimeStampModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow(), nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow(), nullable=True)

class CategoryDB(TimeStampModel):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    book = Relationship("BookDB", back_populates="category", uselist=False, passive_deletes=True)

    def __repr__(self):
        return f"({self.id} {self.title}) "

book_tags_association = Table('book_tag', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class BookDB(TimeStampModel):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    author = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=True)
    category = Relationship("CategoryDB", back_populates="book")
    quantity = Column(Integer, default=1)
    tag = Relationship("Tag", secondary=book_tags_association, back_populates="book")


class Tag(TimeStampModel):
    __tablename__= "tag"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    book = Relationship("BookDB", secondary=book_tags_association, back_populates="tag")



# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
