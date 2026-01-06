from pydantic import BaseModel, Field
from typing import Optional, List
from bson.objectid import ObjectId


class UploadData(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    title: str
    authors: List[str]
    citation: str
    publishedAt: str
    category: List[str]
    abstract: str

    class Config:
        arbitrary_types_allowed = True

class DoUpload(BaseModel):

    file: str
    survey: Optional[bool] = False

    