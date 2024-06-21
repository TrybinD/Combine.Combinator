from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Boolean
from data.db import Base


class DBEvent(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(16), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class DBTeam(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)


class DBUserInSearch(Base):
    __tablename__ = "user_in_search"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)


class DBUserTeamRecommendations(Base):
    __tablename__ = "user_recommendation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    user_in_search_id = Column(Integer, ForeignKey("user_in_search.id"), nullable=False)

