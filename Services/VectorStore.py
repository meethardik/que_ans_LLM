import os
import chromadb
import uuid
from typing import Any
import numpy as np

# Below lines are used only for testing purpose of VectorStore class
# import summarizer as summarizer_object
# from EmbeddingManager import EmbeddingManager

class VectorStore:
    
    def __init__(self, 
                 collection_name: str = "pdf_documents",
                 persist_directory: str = "data/vector_store",
                 documents: list[Any] = [],
                 embeddings: np.ndarray = np.array([])) -> None:
        
        self.documents = documents
        self.embeddings = embeddings
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.chroma_client = None
        self.collection = None
        self.dict_of_metadata = {}
        self._prepare_metadata(documents=documents)
        self._initialize_vector_store()

    def _prepare_metadata(self, documents: list[Any]) -> dict[str, Any]:
        
        try:
            if len(documents) == 0:
                raise ValueError("The documents should not be empty")
            
            for i, doc in enumerate(documents):
                self.dict_of_metadata[f"{i}"] = f"{doc['metadata']}" #dict(documents[i]['metadata'])  #{f"chunk_{i}", doc[0]['metadata']['source']} #doc['metadata']

            return self.dict_of_metadata
        except Exception as e:
            print(f"Error adding documents to the vector store collection '{self.collection_name}': {e}")
            raise e

    def _initialize_vector_store(self):
        try:

            os.makedirs(self.persist_directory, exist_ok=True) # check if the directory exists, if not create it

            # Initialize Chroma client
            self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
            
            # Create or get collection
            self.collection = self.chroma_client.get_or_create_collection(
                    name=self.collection_name,
                    metadata= self.dict_of_metadata #{"description": "Collection of PDF documents embeddings"}
                )

            print(f"Vector store initialized at {self.persist_directory} with collection '{self.collection_name}'")
            print(f"Existing collections count: {self.collection.count()}")
        except Exception as e:
            print(f"Error initializing Chroma collection '{self.collection_name}': {e}")
            raise e

    # def add_documents(self, documents: list[Any], embeddings: np.ndarray):
    def add_documents(self):

        ids = []
        document_text = []
        embedding_list = []
        metadata_collection = []
        
        try:
            if len(self.documents) != len(self.embeddings):
                raise ValueError("The number of documents must match the number of embeddings.")

            for i, (doc, embeddings) in enumerate(zip(self.documents, self.embeddings)):

                # Generate a unique ID for each document                
                doc_id = f"docu_{uuid.uuid4().hex[:8]}_{i}"
                ids.append(doc_id)

                # document content addition
                document_text.append(doc['text'])

                metadata_object = dict(doc['metadata'])  # ensure it's a dict
                metadata_object['doc_index'] = i
                metadata_collection.append(metadata_object)

                # embedding addition
                embedding_list.append(embeddings.tolist())
                
                if self.collection is not None:
                    self.collection.add(
                        ids=ids,
                        documents=document_text,
                        embeddings=embedding_list,
                        metadatas = metadata_collection
                    )
                    

            print(f"The Collection is of type {type(self.collection)}")
            print(f"Added {len(self.documents)} documents to the vector store collection '{self.collection_name}'.")
            print(self.collection)
        except Exception as e:
            print(f"Error adding documents to the vector store collection '{self.collection_name}': {e}")
            raise e

#**********************************************************************************************************
# This is only for the testing purpose of VectorStore class
#**********************************************************************************************************
# embeddings_manager = EmbeddingManager(model_name = "sentence-transformers/all-mpnet-base-v2")
# pdf_chunks = summarizer_object.genreate_pdf_chunks(summarizer_object.load_pdf())
# print(f"Total PDF Chunks: {len(pdf_chunks)}")
# print(pdf_chunks)
# Data_path = "data/pdf"
# generated_texts = [chunk['text'] for chunk in pdf_chunks]
# final_embeddings = embeddings_manager.generate_embeddings(generated_texts)

# vector_store = VectorStore(documents=pdf_chunks, embeddings=final_embeddings)
# vector_store.add_documents()        



    