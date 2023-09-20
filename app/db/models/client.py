from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from ..common.base import _base

class Client(_base):
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company = Column(String)
    address = Column(String)
    time_created = Column(DateTime, server_default=func.now())

    def __init__(self, name, company, address):
        self.name = name
        self.company = company
        self.address = address