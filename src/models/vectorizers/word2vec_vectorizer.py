from pathlib import Path

from navec import Navec
import numpy as np

from .interface import VectorizorInterface


class NavecVectorizor(VectorizorInterface):
    def __init__(self, path_to_navec: Path) -> None:
        """ Vectorizor based on Navec GloVe embeddings

        args:
        - path_to_navec - path to fitted and saved Navec model
        
        """
        self.navec = Navec.load(path_to_navec)
    
    def vectorize(self, descriptions_list):
        descriptions_list = [str(i) for i in descriptions_list]
        def vectorize_text(text):
            tokens = text.split()
            vectors = [self.navec[token] for token in tokens if token in self.navec]
            if vectors:
                return np.mean(vectors, axis=0)
            else:
                return self.navec['<pad>']
        
        return np.array([vectorize_text(description) for description in descriptions_list])