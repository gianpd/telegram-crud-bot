from typing import List, Union
from models.tortoise import Users, Orders
from pypika.terms import Parameter, Interval

#TODO: Do other methods

async def post(payload, users=True) -> int:
    """
    Create Users or Orders raw.
    """
    # element = await Users.create(**payload.dict(exclude_unset=True)) if users \
    #     else await Events.create(**payload.dict(exclude_unset=True))
    element = await Users(**payload) if users else await Orders(**payload)
    await element.save()
    return element.user_id

async def get_users(id: int) -> Union[dict, None]:
    """
    Get Users
    """
    event = await Users.filter(id=id).first().values()
    if event:
        return event
    return None

async def get_orders(id=None) -> Union[dict, None]:
    """
    Get Users
    """
    if id:
        order = await Orders.filter(id=id).first().values()
    else:
        order  = await Orders.filter(timestamp=Parameter('CURRENRT_DATE')-Interval(days=5))
    if order:
        return order
    return None