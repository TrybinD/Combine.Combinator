
from .interface import CombinatorInterface

from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_distances


class DistanceCombinator(CombinatorInterface):
    def __init__(self, distance_threshold: float = 0.5) -> None:
        self.distance_threshold = distance_threshold

    def combine(self, users_embeddings, teams_embeddings):
        users_embeddings = normalize(users_embeddings)
        teams_embeddings = normalize(teams_embeddings)
        
        distances = cosine_distances(users_embeddings, teams_embeddings)
        recomendations = []

        for user, user_distances in enumerate(distances):
            for team, distance in enumerate(user_distances):
                if distance < self.distance_threshold:
                    recomendations.append({"user_id": user, "team_id": team})
        
        return recomendations