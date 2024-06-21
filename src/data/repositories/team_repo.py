from data.models import DBTeam, DBEvent
from data.repositories.base import SQLAlchemyRepository

from sqlalchemy import select
from data.db import SessionLocal

class TeamRepository(SQLAlchemyRepository):
    model = DBTeam

    def get_events(self, **kwargs):
        with SessionLocal() as session:
            stmt = select(DBEvent, self.model).join(self.model).filter_by(**kwargs)
            res = session.execute(stmt)
            session.commit()
            return res.all()