from pydantic import BaseModel,Field
from typing import List, Dict

class Paper(BaseModel):
    title: str = Field(..., description="Title of the paper")
    link: str = Field(..., description="Direct link to the paper's abstract page")
    category: str = Field(..., description="arXiv category code associated with the paper")

class ArxivPapersOutput(BaseModel):
    papers:  List[Paper]