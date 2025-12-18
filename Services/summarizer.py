
from langchain_community.document_loaders import DirectoryLoader ,PyMuPDFLoader
from typing import Any, Dict, List

def load_pdf():
    
    pdf_loader = DirectoryLoader(
        "data/pdf", 
        glob="*.pdf", 
        loader_cls=PyMuPDFLoader, 
        show_progress= False)
    pdf_documents = pdf_loader.load()
    return pdf_documents

def genreate_pdf_chunks(documents: Any, 
                        model_name: str = "gpt-5", 
                        chunk_size: int = 400, 
                        chunk_size_overlap: int=50) -> List[Dict]:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(model_name=model_name,
                                                                         chunk_size=chunk_size,
                                                                         chunk_overlap=chunk_size_overlap)
    chunked_docs = text_splitter.split_documents(documents)

    chuked_pdf = []
    for i, doc in enumerate(chunked_docs):
        chuked_pdf.append({
            "id": f"chunk_{i}",
            "text": doc.page_content.strip(),
            "metadata": doc.metadata,
            "source": doc.metadata.get("source", ""),
            "page_number": doc.metadata.get("page_number", -1)
        })
    return chuked_pdf