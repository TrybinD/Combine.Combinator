from typing import Dict, Any

from models.combinators.interface import CombinatorInterface
from models.vectorizers.interface import VectorizorInterface


class RecommendationService:
    def __init__(self, vectorizer: VectorizorInterface, combinator: CombinatorInterface):
        self.vectorizer = vectorizer
        self.combinator = combinator

    def get_recommendations(self, users_descriptions: Dict[str, Any], k_recs: int, n_users_in_project: int):
        index_mapping = {}
        descriptions_list = []

        for i, (index, description) in enumerate(users_descriptions.items()):
            index_mapping[i] = index
            descriptions_list.append(str(description))

        embeddings = self.vectorizer.vectorize(descriptions_list)

        combinations, projects = self.combinator.combine(embeddings, k_recs, n_users_in_project)

        users_recos = {index_mapping[i]: recos for i, recos in enumerate(combinations)}
        projects = {i: proj for i, proj in enumerate(projects)}

        return users_recos, projects
