from pydantic import BaseModel
from typing import Optional

class AIServices(BaseModel):

    service: str
    input_text: str
    target_language: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
