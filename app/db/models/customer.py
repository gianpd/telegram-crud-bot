from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from ..common.base import _base

class Customer(_base):
    __tablename__ = "customer"
    
    id = Column(Integer, primary_key=True, autoincrement='auto')
    customer_number = Column(String(255), unique=True)
    name = Column(String(255))
    company = Column(String(255))
    address = Column(String(255))
    last_seen = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


    def __repr__(self):
        return f"<Customer {self.name}>"