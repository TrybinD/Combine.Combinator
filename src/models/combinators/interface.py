from abc import ABC, abstractmethod

class CombinatorInterface(ABC):
    
    @abstractmethod
    def combine(self, users_embeddings, teams_embeddings):
        raise NotImplementedError