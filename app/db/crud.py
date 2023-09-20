import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger('TGCRUD-logger')

from uuid import uuid4
from datetime import date

from .models.client import Client
from .models.order import Order
from .common.base import get_session

from sqlalchemy import Date, cast, select

import typing

def create_client(name: str, company: str, address: str)->None:
    session = get_session()
    client = Client(name, company, address)
    session.add(client)
    session.commit()
    session.close()


def delete_client(name, company):
    session = get_session()
    session.query(Client)\
        .filter(Client.name==name, Client.company==company)\
            .delete(synchronize_session=False)
    session.commit()
    session.close()

def delete_all_clients():
    session = get_session()
    session.query(Client).delete()
    session.commit()
    session.close()



def create_order(product_name: str, quantity: int, clients: typing.List[Client])->str:
    session = get_session()
    order_number = uuid4().hex[:15]
    order = Order(order_number, product_name, quantity, clients)
    logger.info(f'Adding the order {order_number} to the Order table ...')
    session.add(order)
    session.commit()
    session.close()
    return order_number

def get_clients():
    session = get_session()
    clients = session.query(Client).all()
    session.close()
    return clients


def get_clients_datetime(_date: date):
    session = get_session()
    clients = session.query(Client).filter(cast(Client.time_created, Date) >= _date).all()
    session.close()
    return clients

def get_order_by_product_name(product_name):
    session = get_session()
    orders = session.query(Order).filter(Order.product_name==product_name).all()
    return orders




