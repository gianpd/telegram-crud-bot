import os
import sys

from typing import Union, List

from tortoise import Tortoise

from db import crud
from db.models.tortoise import Order_pydantic, User_pydantic


import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("db-ingest")



TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "app": {
        "models": {
            # "models": ["models.tortoise", "aerich.models"],
            "models": ["./models.tortoise"],
            "default_connection": "default",
        },
    },
}



async def run_insert(row, user=True):
    print('Starting db with conf')
    print(TORTOISE_ORM)
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    i = await crud.post(row, user=user)
    # row = await crud.get_user(i)
    return i

