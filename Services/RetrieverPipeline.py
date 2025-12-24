from typing import Any, List, Dict
from EmbeddingManager import EmbeddingManager
from VectorStore import VectorStore
from scipy.spatial import distance

import chromadb

# import summarizer as summarizer_object
# from EmbeddingManager import EmbeddingManager

class RetrieverPipeline:
    
    def __init__(self, vector_store: chromadb.Collection, embeddings: EmbeddingManager):
        self.vector_store = vector_store
        self.embeddings = embeddings

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        print(f"Retrieving top {top_k} documents for the query: {query}")

        # Generate embedding for the query
        query_embedding = self.embeddings.generate_embeddings([query])[0]
        query_flatten_vector = query_embedding.flatten()

        if query_embedding.size == 0:
            print("Failed to generate embedding for the query.")
            return []
        try:
            
            retrieved_docs = []
            documents_text = []
            metadata_text = []
            ids = []
            distances = []
            map_doc_score = {}
            final_retrieved_docs = []

            if self.vector_store:
                results = self.vector_store.query(query_embeddings = [query_embedding.tolist()], n_results=top_k)
                
                if (results['documents'] and len(results['documents']) > 0) and (results['ids'] and len(results['ids']) > 0) and (results['distances'] and len(results['distances']) > 0 and (results['metadatas']) and len(results['metadatas']) > 0):
                    documents_text = results['documents'][0]
                    ids = results['ids'][0]
                    distances = results['distances'][0]
                    metadata_text = results['metadatas'][0]

                    for i, (docId, documents, distnace, metadatas) in enumerate(zip(ids, documents_text, distances, metadata_text)):
                        retrieved_docs.append({
                            "id": docId,
                            "text": documents,
                            "distance": distnace,
                            "metadata": metadatas,
                            "rank": i + 1
                        })

            if self.embeddings is not None and self.embeddings.model is not None:

                for doc in retrieved_docs:
                    
                    doc_embedding = self.embeddings.generate_embeddings([doc['text']])[0]
                    doc_flatten_vector = doc_embedding.flatten()
                    
                    # Calculate similarity score (e.g., cosine similarity)  
                    score = 1 - distance.cosine(query_flatten_vector, doc_flatten_vector)
                    map_doc_score[score] = doc['text']

                    final_retrieved_docs.append({
                        "text": doc['text'],
                        "similarity_score": score,
                        "metadata": doc['metadata']
                    })
                
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []
        
        return final_retrieved_docs

#**********************************************************************************************************
# This is only to test the RetrieverPipeline class
#**********************************************************************************************************
# embeddings_manager = EmbeddingManager(model_name = "all-MiniLM-L6-v2") #sentence-transformers/all-mpnet-base-v2
# pdf_chunks = summarizer_object.genreate_pdf_chunks(summarizer_object.load_pdf())
# print(f"Total PDF Chunks: {len(pdf_chunks)}")
# print(pdf_chunks)
# Data_path = "data/pdf"
# generated_texts = [chunk['text'] for chunk in pdf_chunks]
# final_embeddings = embeddings_manager.generate_embeddings(generated_texts)

# vector_store = VectorStore(documents=pdf_chunks, embeddings=final_embeddings)
# vector_store.add_documents()   

# rag_retriever_pipeline = RetrieverPipeline(vector_store=vector_store, embeddings= embeddings_manager)

# results = rag_retriever_pipeline.retrieve("What professional skills are needed for Integration Architect", 4)
# print(f"Retrieved {len(results)} documents:")
# for doc in results:
#     print(doc)
