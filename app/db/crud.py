from typing import List, Union
from db.models.tortoise import User, Order

#TODO: Do other methods

async def post(payload, user=True) -> int:
    """
    Create Users or Orders raw."""

    element = await User(**payload) if user else await Order(**payload)
    await element.save()
    return element.user_id

async def get_user(id: int) -> Union[dict, None]:
    """
    Get Users
    """
    event = await User.filter(id=id).first().values()
    if event:
        return event
    return None