from langchain_openai import OpenAI
from openai import OpenAI
from RetrieverPipeline import RetrieverPipeline
import os
import sys

from dotenv import load_dotenv

# This is just for testing this particular file independently
# import summarizer as summarizer_object
# from EmbeddingManager import EmbeddingManager
# from VectorStore import VectorStore

if os.getenv("ENVIRONMENT") == "development":
    print("Loading environment variables from .env file")
    load_dotenv(".env")

sys.path.append("Infrastructure")
from Infrastructure.configuration import GetConfiguration

class RagUsingLLM:
    
    def __init__(self, query: str, retriever_object: RetrieverPipeline, top_k: int = 5):
        self.retriever_object = retriever_object
        self.query = query
        self.top_k = top_k
    
    
    def generate_response_using_llm(self):

        try:
            openai_api_key = None

            keyvault_name = os.getenv("KeyVault_Name")
            secret_name = os.getenv("secret_name")

            if keyvault_name and secret_name:
                config = GetConfiguration(secret_name=secret_name, keyvault_name=keyvault_name)
                openai_api_key = config.get_openai_api_key()
            
            if not openai_api_key:
                raise ValueError("OpenAI API key is not provided. Please set the OPENAI_API_KEY environment variable.")
            
            llm = OpenAI(api_key = openai_api_key)

            retrieved_docs = self.retriever_object.retrieve(query=self.query, top_k=self.top_k)

            if not retrieved_docs or len(retrieved_docs) == 0:
                print("No relevant documents found for the query.")
                return "I'm sorry, I couldn't find any relevant information to answer your query."
            else:
                context = "\n\n".join([doc['text'] for doc in retrieved_docs])

            system_prompt = ("You are a helpful assistant that provides accurate and concise answers based on the provided context."
                             "If the answer is not contained within the context, respond with 'I don't know.'")
            
            model_name = os.getenv('Model')
            if model_name and len(model_name.strip()) > 0:
                response = llm.chat.completions.create(model=model_name,
                                                    messages=[{"role": "system", "content": system_prompt},
                                                                {"role": "user", "content": f"Context: {context}\n\nQueston: {self.query}\nAnswer:"}])
                return response

        except Exception as e:
            print(f"Error generating response using LLM: {e}")
            return ""
        
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

# rag_using_llm = RagUsingLLM(query="What professional skills are needed for Integration Architect", 
#                             retriever_object=rag_retriever_pipeline, 
#                             top_k=3)
# response_from_llm = rag_using_llm.generate_response_using_llm()
# print("Response from LLM:")

# print(response_from_llm.choices[0].message.content)