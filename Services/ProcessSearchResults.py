from VectorStore import VectorStore
from EmbeddingManager import EmbeddingManager

class ProcessSearchResults:
    
    def __init__(self) -> None:
        pass

    def process_results(self):

        try:

            VectorStore_instance = VectorStore()
            EmbeddingManager_instance = EmbeddingManager()

            VectorStore_instance.get_vector_collection("pdf_documents", "data/vector_store")
            