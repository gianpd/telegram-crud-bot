from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..common.base import _base


class Order(_base):
    """One-to-Many Customer-Orders Data model"""
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id')) # SQL relathionship
    order_number = Column(String(255), unique=True)
    product_name = Column(String(255))
    quantity = Column(Integer)
    last_seen = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    customer = relationship("Customer") # App models relathionship

    def __repr__(self):
        return f"<Order {self.order_number}>"