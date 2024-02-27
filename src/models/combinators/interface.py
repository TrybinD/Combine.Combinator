from abc import ABC, abstractclassmethod

class CombinatorInterface(ABC):
    
    @abstractclassmethod
    def combine(self, embeddings, k_recs: int, n_users_in_project: int):
        raise NotImplementedError