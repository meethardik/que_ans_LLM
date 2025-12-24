import os
import chromadb

class UtilityVectorStore:
    def __init__(self, collection_name: str, persist_directory: str):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.chroma_client = None

    def get_vector_collection(self) -> chromadb.Collection:
        try:

            os.makedirs(self.persist_directory, exist_ok=True) # check if the directory exists, if not create it

            # Initialize Chroma client
            chroma_client = chromadb.PersistentClient(path=self.persist_directory)
            
            # Create or get collection
            vector_collection = chroma_client.get_collection(
                    name=self.collection_name,
                )

            return vector_collection
        except Exception as e:
            print(f"Error getting collection '{self.collection_name}': {e}")
            raise e