
import numpy as np

from .interface import CombinatorInterface

class RandomCombinator(CombinatorInterface):
    def __init__(self, random_treshold: float = 0.5) -> None:
        self.random_treshold = random_treshold

    def combine(self, users_embeddings, teams_embeddings):

        recomendations = []

        for user, user_emb in enumerate(users_embeddings):
            for team, team_emb in enumerate(teams_embeddings):
                if np.random.rand() < self.random_treshold:
                    recomendations.append({"user_id": user,
                                           "team_id": team})
                    
        
        return recomendations

