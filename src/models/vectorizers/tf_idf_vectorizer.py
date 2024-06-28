from pathlib import Path
from typing import Union
import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

from .interface import VectorizorInterface

Vectorizor = Union[CountVectorizer, TfidfVectorizer, HashingVectorizer]

class SklearnVectorizor(VectorizorInterface):
    def __init__(self, path_to_vectorizor: Path) -> None:
        """ Vectorizor based on Vectorizors from Sklearn - CountVectorizer, TfidfVectorizer, HashingVectorizer

        args:
        - path_to_vectorizor - path to fitted and saved vectorizor from sklearn
        
        """
        self.vectorizor: Vectorizor = joblib.load(path_to_vectorizor)

        if not hasattr(self.vectorizor, "transform"):
            raise TypeError(f"Object {path_to_vectorizor} dosn`t have 'transform' method")
    
    def vectorize(self, descriptions_list):
        descriptions_list = [str(i) for i in descriptions_list]

        res = self.vectorizor.transform(descriptions_list)

        return res