
import numpy as np

from .interface import VectorizorInterface

class RandomVectorizor(VectorizorInterface):
    def __init__(self, n_dims: int) -> None:
        self.n_dims = n_dims
    
    def vectorize(self, descriptions_list):
        n = len(descriptions_list)

        res = np.random.random(size=(n, self.n_dims))

        return res