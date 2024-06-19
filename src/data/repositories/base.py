from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update

from data.db import SessionLocal


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def add(self, data: dict) -> int:
        with SessionLocal() as session:
            try:
                stmt = insert(self.model).values(**data).returning(self.model.id)
                res = session.execute(stmt).scalar_one()
                session.commit()
                return res
            except Exception as e:
                session.rollback()
                raise e
    
    def get(self, **kwargs):
        with SessionLocal() as session:
            stmt = select(self.model).filter_by(**kwargs)
            results = session.execute(stmt)
            results = results.scalars().all()
            return results
        
    def update(self, data: dict, **kwargs):
        with SessionLocal() as session:
            stmt = update(self.model).filter_by(**kwargs).values(**data)
            session.execute(stmt)
            session.commit()
