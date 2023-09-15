import os
import sys

from typing import Union, List

from tortoise import Tortoise

import crud
from models.tortoise import Events_pydantic, Users_pydantic


import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("db-ingest")

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            # "models": ["models.tortoise", "aerich.models"],
            "models": ["models.tortois"],
            "default_connection": "default",
        },
    },
}

async def run_insert(row):
    pass
