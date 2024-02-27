
import numpy as np

from .interface import CombinatorInterface
from data.repo.interface import ReadableRepoInterface

class RandomCombinator(CombinatorInterface):
    def __init__(self, project_repo: ReadableRepoInterface) -> None:
        self.project_repo = project_repo

    def combine(self, embeddings, k_recs: int, n_users_in_project: int):
        
        n = len(embeddings)

        recs = [[] for i in range(n)]
        space_left = np.array([k_recs for _ in range(n)])

        rec_to_n_users = n_users_in_project

        project_i = 0
        users = []
        while space_left.sum() != 0:
            users = np.random.choice(a=n, size=min(rec_to_n_users, (space_left!=0).sum()), p=space_left/space_left.sum(), replace=False)
            for user in users:
                recs[user].append(project_i)
                space_left[user] -= 1
            project_i += 1
        
        projects = self.get_random_projects(n_projects=project_i)
            
        return recs, projects
    
    def get_random_projects(self, n_projects):

        all_projects = self.project_repo.get_all()

        projects = np.random.choice(all_projects, size=n_projects, replace=False)

        return [p.description for p in projects]
