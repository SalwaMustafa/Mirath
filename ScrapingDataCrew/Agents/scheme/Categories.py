from pydantic import BaseModel,Field
from typing import List, Dict

class CategoryPaperQueries(BaseModel):
    categories: Dict[str, List[str]]
    
