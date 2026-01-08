from pydantic import BaseModel


class Search(BaseModel):

    question: str

    class Config:
        arbitrary_types_allowed = True