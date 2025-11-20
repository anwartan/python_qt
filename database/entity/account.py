from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
class Account(Base):
    __tablename__ = 'accounts'
    
    id=Column(Integer,primary_key=True)
    site=Column(String,nullable=False)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)