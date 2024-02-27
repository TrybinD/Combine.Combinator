from abc import ABC, abstractmethod


class ReadableRepoInterface(ABC):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def filter(self, **kwargs):
        raise NotImplementedError
    
class ChangeableRepoInterface(ABC):

    @abstractmethod
    def create(self, data):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id, data):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
    