from pydantic import BaseModel


class Search(BaseModel):

    question: str
    limit: int

    class Config:
        arbitrary_types_allowed = True