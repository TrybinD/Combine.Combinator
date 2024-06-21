from data.models import DBUserInSearch, DBEvent
from data.repositories.base import SQLAlchemyRepository

from sqlalchemy import select
from data.db import SessionLocal

class UserInSearchRepository(SQLAlchemyRepository):
    model = DBUserInSearch

    def get_events(self, **kwargs):
        with SessionLocal() as session:
            stmt = select(DBEvent, self.model).join(self.model).filter_by(**kwargs)
            res = session.execute(stmt)
            session.commit()
            return res.all()