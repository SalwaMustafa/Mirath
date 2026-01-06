from pydantic import BaseModel,Field
from typing import List, Dict

class Paper(BaseModel):
    title: str = Field(..., description="Title of the paper")
    authors: List[str] = Field(..., description="List of authors of the paper")
    citation: str = Field(..., description="Citation information for the paper")
    publichedAt:str = Field(..., description="Publication date of the paper")
    category: List[str] = Field(..., description="arXiv categories associated with the paper")
    abstract: str = Field(..., description="Abstract of the paper")
    content: List[str] = Field(..., description="Full HTML content of the paper")

class ScrapePapersOutput(BaseModel):
    papers:List[Paper]