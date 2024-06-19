from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

import config

sync_engine = create_engine(config.SYNC_CONNECTION_STRING)
SessionLocal = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
        
def create_db():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
