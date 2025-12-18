from pydantic import BaseModel

class PDF_Chunk(BaseModel):
    id: str
    text: str
    metadata: str
    source: str
    page_number: int

class RetrievedDocs(BaseModel):
    docs: list[dict[str, any]]

class AdvancedRAGOutput(BaseModel):
    answer: str
    confidence_score: float
    sources: list[str]