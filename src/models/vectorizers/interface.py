from abc import ABC, abstractclassmethod

class VectorizorInterface(ABC):
    
    @abstractclassmethod
    def vectorize(self, descriptions_list):
        raise NotImplementedError