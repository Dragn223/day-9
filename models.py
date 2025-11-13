from sqlalchemy import Column, Integer, String, Float
from db import Base


class Book(Base):
    __tablename__ = "book2"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publisher = Column(String, index=True)
    year = Column(Integer)
    price = Column(Float)
