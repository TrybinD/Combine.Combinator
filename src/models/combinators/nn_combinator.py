

from pathlib import Path

import torch
from .interface import CombinatorInterface

class NNCombinator(CombinatorInterface):
    def __init__(self, model_path: Path, threshold: float = 0.5, device = "cpu") -> None:
        self.model = torch.load(model_path)
        self.model.eval()
        self.model.to(device)
        self.threshold = threshold
        self.device = device

    def combine(self, users_embeddings, teams_embeddings):
        users_embeddings = torch.tensor(users_embeddings, dtype=torch.float32, device=self.device)
        teams_embeddings = torch.tensor(teams_embeddings, dtype=torch.float32, device=self.device)
        
        recommendations = []
        
        with torch.no_grad():
            for user_idx, user_emb in enumerate(users_embeddings):
                for team_idx, team_emb in enumerate(teams_embeddings):
                    combined_input = torch.cat((user_emb, team_emb)).unsqueeze(0)
                    score = self.model(combined_input).item()
                    if score >= self.threshold:
                        recommendations.append({"user_id": user_idx, "team_id": team_idx})

        return recommendations