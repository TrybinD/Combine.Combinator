
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity


from .interface import CombinatorInterface

class DiversityCombinator(CombinatorInterface):
    def __init__(self, similarity_threshold: float = 0.5, diversity_factor: float = 0.3) -> None:
        self.similarity_threshold = similarity_threshold
        self.diversity_factor = diversity_factor

    def combine(self, users_embeddings, teams_embeddings):
        users_embeddings = normalize(users_embeddings)
        teams_embeddings = normalize(teams_embeddings)
        
        similarities = cosine_similarity(users_embeddings, teams_embeddings)
        recommendations = []

        for user_idx, user_similarities in enumerate(similarities):
            user_recommendations = []
            for team_idx, similarity in enumerate(user_similarities):
                if similarity >= self.similarity_threshold:
                    user_recommendations.append((team_idx, similarity))

            user_recommendations.sort(key=lambda x: x[1], reverse=True)
            
            diversified_recommendations = []
            for i, (team_idx, similarity) in enumerate(user_recommendations):
                if i == 0 or all(cosine_similarity([teams_embeddings[team_idx]], [teams_embeddings[rec['team_id']]])[0, 0] < self.diversity_factor for rec in diversified_recommendations):
                    diversified_recommendations.append({"user_id": user_idx, "team_id": team_idx})

            recommendations.extend(diversified_recommendations)
        
        return recommendations