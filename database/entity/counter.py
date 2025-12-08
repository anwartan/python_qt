from calendar import c
from sympy import use
from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
class Counter(Base):
    __tablename__ = 'counter'
    id = Column(Integer, primary_key=True)
    tipe = Column(String, nullable=False)
    tanggal = Column(Date, nullable=False)
    jumlah_telur = Column(Integer, nullable=False)
    jumlah_telur_rusak = Column(Integer, nullable=False)