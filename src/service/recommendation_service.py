from typing import Dict, Any

from models.combinators.interface import CombinatorInterface
from models.vectorizers.interface import VectorizorInterface


class UserTeamRecommendationService:
    def __init__(self, 
                 users_vectorizer: VectorizorInterface,
                 teams_vectorizer: VectorizorInterface,
                 combinator: CombinatorInterface):
        self.users_vectorizer = users_vectorizer
        self.teams_vectorizer = teams_vectorizer
        self.combinator = combinator

    def get_recommendations(self, users_descriptions: Dict[int, str], teams_descriptions: Dict[int, str]):

        users_descriptions_list, users_id_mappings = self._get_descriptions_list(users_descriptions)
        teams_descriptions_list, teams_id_mappings = self._get_descriptions_list(teams_descriptions)

        users_embeddings = self.users_vectorizer.vectorize(users_descriptions_list)
        teams_embeddings = self.teams_vectorizer.vectorize(teams_descriptions_list)

        combinations = self.combinator.combine(users_embeddings, teams_embeddings)

        recommendations = [{"user_id": users_id_mappings[combination["user_id"]],
                            "team_id": teams_id_mappings[combination["team_id"]]} for combination in combinations]

        return recommendations
    
    def _get_descriptions_list(self, descriptions):
        index_mapping = {}
        descriptions_list = []

        for i, (entity_id, description) in enumerate(descriptions.items()):
            index_mapping[i] = entity_id
            descriptions_list.append(description)

        return descriptions_list, index_mapping
