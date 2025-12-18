from sentence_transformers import SentenceTransformer
import numpy as np
import summarizer as sb

class EmbeddingManager:
    
    def __init__(self, model_name : str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        
        try:
            
            print(f"Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model {self.model_name} loaded successfully. The Embedding dimension is {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            self.model_name = "all-MiniLM-L6-v2"
            raise e
    
    def generate_embeddings(self, text: list[str]) -> np.ndarray:
        
        embeddings = np.array([])
        if self.model is not None:
            embeddings = self.model.encode(text, show_progress_bar=True)
        else:
            self._load_model()
        
        return embeddings
        
#**********************************************************************************************************
# This is only for the testing purpose of Embedding Manager class
#**********************************************************************************************************    
# embeddings_manager = EmbeddingManager(model_name = "sentence-transformers/all-mpnet-base-v2")
# pdf_chunks = sb.genreate_pdf_chunks(sb.load_pdf())
# print(f"Total PDF Chunks: {len(pdf_chunks)}")
# print(pdf_chunks)
# Data_path = "data/pdf"
# embeddings = embeddings_manager.generate_embeddings([chunk['text'] for chunk in pdf_chunks])
# print(f"Generated Embeddings shape: {embeddings.shape}")

