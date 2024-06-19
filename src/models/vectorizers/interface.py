from abc import ABC, abstractmethod

class VectorizorInterface(ABC):
    
    @abstractmethod
    def vectorize(self, descriptions_list):
        raise NotImplementedError