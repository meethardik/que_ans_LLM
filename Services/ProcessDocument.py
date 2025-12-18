import os

from Services.VectorStore import VectorStore
import Services.summarizer as summarizer_object
from Services.EmbeddingManager import EmbeddingManager

class ProcessDocument:

    def __init__(self):
        pass

    def process(self):

        try:
            print("Starting document processing...")
            # Load PDF and generate chunks
            pdf_chunks = summarizer_object.genreate_pdf_chunks(summarizer_object.load_pdf())
            generated_texts = [chunk['text'] for chunk in pdf_chunks]

            # Generate embeddings
            transformer_model_name = os.getenv("TRANSFORMER_MODEL_NAME")
            embeddings_manager = EmbeddingManager(model_name = transformer_model_name)
            final_embeddings = embeddings_manager.generate_embeddings(generated_texts)

            # Create Vector Store and add documents
            vector_store = VectorStore(documents=pdf_chunks, embeddings=final_embeddings)
            vector_store.add_documents()   
            print("Document processing completed successfully.")
        except Exception as e:
            print(f"Error during document processing: {e}")