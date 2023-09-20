import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'))
_sessionFactory = sessionmaker(bind=engine)
_base = declarative_base()

def get_session():
    _base.metadata.create_all(engine)
    return _sessionFactory()