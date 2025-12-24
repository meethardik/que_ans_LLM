#from VectorStore import VectorStore
from EmbeddingManager import EmbeddingManager
from RetrieverPipeline import RetrieverPipeline
from openai import OpenAI

import os
import sys
import chromadb

class ProcessSearchResults:
    
    def __init__(self, query: str, top_k: int) -> None:
        self.query = query
        self.top_k = top_k

    def _initialize_vector_store(self) -> chromadb.Collection:

        sys.path.append('Utilities')
        from Utilities.utility_vector_store import UtilityVectorStore

        vectorstore_instance = UtilityVectorStore(collection_name="pdf_documents", persist_directory="data/vector_store")

        return_value = vectorstore_instance.get_vector_collection()
        return return_value
        
    def _intitialize_embedding_manager(self) -> EmbeddingManager:
        embedding_manager = EmbeddingManager(model_name=os.getenv("Embedding_Model_Name", "all-MiniLM-L6-v2"))
        return embedding_manager
    
    def _initialize_retriever_pipeline(self, 
                                       vector_store: chromadb.Collection, 
                                       embeddings: EmbeddingManager) -> RetrieverPipeline:
        retrieverpipeline_instance = RetrieverPipeline(
            vector_store=vector_store, embeddings=embeddings)
        return retrieverpipeline_instance
    
    def _retrieve_openai_api_key(self) -> str:

        openai_api_key = None
        keyvault_name = os.getenv("KeyVault_Name")
        secret_name = os.getenv("secret_name")

        sys.path.append('Infrastructure')
        from Infrastructure.configuration import GetConfiguration

        if keyvault_name and secret_name:
            config = GetConfiguration(secret_name=secret_name, keyvault_name=keyvault_name)
            openai_api_key = config.get_openai_api_key()
        
        if openai_api_key:
            return openai_api_key
        
        return ""

    def _initialize_llm(self) -> OpenAI:

        openai_api_key = self._retrieve_openai_api_key()
        llm = OpenAI(api_key = openai_api_key)
        return llm

    def process_query_results(self):

        try:

            vectorstore_instance = self._initialize_vector_store()
            embedding_manager = self._intitialize_embedding_manager()
            retrieverpipeline_instance = self._initialize_retriever_pipeline(
                vector_store=vectorstore_instance, embeddings=embedding_manager)
            
            results = retrieverpipeline_instance.retrieve(self.query, self.top_k)

            if not results or len(results) == 0:
                return "I'm sorry, I couldn't find any relevant information to answer your query."
            
            system_prompt = ("You are a helpful assistant that provides accurate and concise answers based on the provided context. "
            "If the answer is not contained within the context, respond with 'I don't know.'")

            model_name = os.getenv('Model', 'gpt-5')
            if model_name and len(model_name.strip()) > 0:
                llm = self._initialize_llm()

                context = "\n\n".join([doc['text'] for doc in results])

                response = llm.chat.completions.create(model=model_name,
                                                    messages=[{"role": "system", "content": system_prompt},
                                                              {"role": "user", "content": f"Context: {context}\n\nQuestion: {self.query}"}])
                
                answer = response.choices[0].message.content
                return answer
        except Exception as e:
            print(f"Error processing query results: {e}")
            raise e
        

