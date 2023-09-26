import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine(os.environ.get('DATABASE_URL'))
Base.metadata.create_all(engine)
_sessionFactory = sessionmaker(engine)

def get_session():
    return _sessionFactory()
