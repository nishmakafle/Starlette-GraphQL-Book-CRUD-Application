from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        create_engine, inspect)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship, sessionmaker

from models import Base, engine, TimeStampModel


class User(TimeStampModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    profile = Relationship("UserProfile", uselist=False, back_populates="user")

    

    

class UserProfile(TimeStampModel):
    __tablename__= "profile"

    id = Column(Integer, primary_key=True, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    image = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    dob = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True, nullable=False)
    user = Relationship("User", back_populates="profile")



    def __repr__(self):
        return f"{self.firstname} + {self.lastname}"
    