from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..common.base import _base

association_table = Table(
    'association_client_order', _base.metadata,
    Column('client_id', Integer, ForeignKey('client.id')),
    Column('order_id', Integer, ForeignKey('order.id'))
)

class Order(_base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    order_number = Column(String)
    product_name = Column(String)
    quantity = Column(Integer)
    time_created = Column(DateTime, server_default=func.now())
    clients = relationship('Client', secondary=association_table)

    def __init__(self, order_number, product_name, quantity, clients):
        self.order_number = order_number
        self.product_name = product_name
        self.quantity = quantity
        self.clients = clients