from sympy import use
from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey,Date,Integer
class Egg(Base):
    __tablename__ = 'Egg'
    id = Column(Integer, primary_key=True)
    tanggal = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    jumlah = Column(Integer, nullable=False)
    rusak = Column(Integer, nullable=False)