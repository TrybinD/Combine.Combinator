
import torch
from transformers import AutoTokenizer, AutoModel

from .interface import VectorizorInterface


class BERTVectorizor(VectorizorInterface):
    def __init__(self, model_name_or_path: str) -> None:
        """ Vectorizor based on BERT-like models from Hugging Face transformers

        args:
        - model_name_or_path - path to the pre-trained and saved BERT model or its name in Hugging Face model hub
        
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModel.from_pretrained(model_name_or_path)
    
    def vectorize(self, descriptions_list):
        descriptions_list = [str(i) for i in descriptions_list]
        inputs = self.tokenizer(descriptions_list, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Use the [CLS] token embeddings for classification tasks
        cls_embeddings = outputs.last_hidden_state[:, 0, :]

        return cls_embeddings.numpy()
