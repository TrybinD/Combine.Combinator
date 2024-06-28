import joblib
import numpy as np
from pathlib import Path


from .interface import CombinatorInterface


class XGBoostCombinator(CombinatorInterface):
    def __init__(self, model_path: Path, preprocessor_path: Path, threshold: float = 0.5) -> None:
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        self.threshold = threshold

    def combine(self, users_embeddings, teams_embeddings):
        users_embeddings = self.preprocessor.transform_users(users_embeddings)
        teams_embeddings = self.preprocessor.transform_teams(teams_embeddings)
        
        recommendations = []
        
        for user_idx, user_emb in enumerate(users_embeddings):
            for team_idx, team_emb in enumerate(teams_embeddings):
                combined_input = np.concatenate((user_emb, team_emb)).reshape(1, -1)
                score = self.model.predict_proba(combined_input)[0, 1]
                if score >= self.threshold:
                    recommendations.append({"user_id": user_idx, "team_id": team_idx})

        return recommendations