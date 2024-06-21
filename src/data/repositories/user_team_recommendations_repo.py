from data.models import DBUserTeamRecommendations
from data.repositories.base import SQLAlchemyRepository

class UserTeamRecommendationsRepository(SQLAlchemyRepository):
    model = DBUserTeamRecommendations