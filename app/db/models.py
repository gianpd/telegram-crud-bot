from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from .common.base import Base

from datetime import datetime
from typing import List, Optional


class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now())
    order_items = relationship(
        "OrderItem", cascade="all, delete-orphan", backref="order"
    )

    def __repr__(self):
        return "Oder(%r, %r)" % (self.order_id, self.customer_name)

class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    description = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return "Item(%r, %r)" % (self.description, self.price)


class OrderItem(Base):
    __tablename__ = "orderitem"
    order_id = Column(Integer, ForeignKey("order.order_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    price = Column(Float, nullable=False)

    item = relationship(Item, lazy="joined")

    def __repr__(self):
        return f"<Order {self.id}-{self.order_number}>"