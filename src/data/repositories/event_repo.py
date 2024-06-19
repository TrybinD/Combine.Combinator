from data.models import DBEvent
from data.repositories.base import SQLAlchemyRepository

class EventRepository(SQLAlchemyRepository):
    model = DBEvent
