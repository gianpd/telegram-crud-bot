import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger('TGCRUD-logger')

from uuid import uuid4
from datetime import date

from .models import Customer, Order
from .common.base import get_session

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2.errors import UndefinedColumn
from typing import List, Optional


def create_customer(customer: Customer) -> Optional[Customer]:
    """Create customer method: check if the customer is not already present in the DB.
       If not, create it and commit.
       
       --Params
        - session: SQLAlchemy DB Session
        - customer: Customer model object
        
       --Return
        - Optional[Customer]
    """
    try:
        session = get_session()
        existing_customer = session.query(Customer)\
            .filter(Customer.customer_number == customer.customer_number).first()
        if not existing_customer:
            session.add(customer)
            session.commit()
            logger.info(f'Customer {customer.customer_number} created.')
            response = session.query(Customer).filter(Customer.customer_number==customer.customer_number).first()
            session.close()
            return response
        else:
            logger.info(f'Customer {existing_customer.customer_number} already exists.')
            session.close()
            return existing_customer.id
    except IntegrityError as e:
        logger.error(e.orig)
        raise e.orig
    except UndefinedColumn as e:
        logger.error(e)
        raise e
    except SQLAlchemyError as e:
        logger.error(f'Unexpected error when creating customer: {e}')
        raise e
    

    
def create_order(order: Order) -> Optional[Order]:
    """Create order method: check if the given order is not already present in the DB.
       If not, create it and commit.
       
       --Params
        - session: SQLAlchemy DB Session
        - order: Order model object
        
       --Return
        - Optional[Order]
    """
    # try:
    session = get_session()
    logger.info(f'create_order> {order.__dict__}')
    r = session.query(Order).all()
    logger.info(r)
    #     existing_order = session.query(Order)\
    #         .filter(Order.order_number == order.order_number).first()
    #     if not existing_order:
    #         session.add(order)
    #         session.commit()
    #         logger.info(f'Order {order.order_number} created.')
    #     else:
    #         logger.info(f'Order {order.order_number} already exists.')
    #     response = session.query(Order).filter(Order.order_number==order.order_number).first()
    #     session.close()
    #     return response
    # except IntegrityError as e:
    #     logger.error(e.orig)
    #     raise e.orig
    # except UndefinedColumn as e:
    #     logger.error(e)
    #     raise e
    # except SQLAlchemyError as e:
    #     logger.error(f'Unexpected error when creating order: {e}')
    #     raise e

def get_all_customers():
    """Fetch all customers"""
    session = get_session()
    customers = (
        session.query(Customer).all()
    )
    session.close()
    for customer in customers:
        payload = {
            "customer_number": customer.customer_number,
            "name": customer.name,
            "company": customer.company,
            "address": customer.address,
            "created": customer.created_at
        }
        yield payload

def get_all_orders(customer: Customer):
    """Fetch all orders belonging to the given customer"""
    session = get_session()
    orders = (
        session.query(Order)\
            .join(Customer, Order.customer_id==customer.id)\
            .filter(customer_number=customer.customer_number)\
            .all() 
    )
    session.close()
    for order in orders:
        payload = {
            "order_number": order.order_number,
            "product_name": order.product_name,
            "quantity": order.quantity,
            "created": order.created_at,
            "customer": {
                "name": order.customer.name,
                "company": order.customer.company,
                "address": order.customer.address
            }
        }
        yield payload






