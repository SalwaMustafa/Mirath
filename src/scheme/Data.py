from pydantic import BaseModel, Field
from typing import Optional, List
from bson.objectid import ObjectId


class UploadData(BaseModel):

    mongo_id: Optional[ObjectId] = Field(None, alias="_id")
    id: str
    title: str
    authors: List[str]
    citation: str
    publishedAt: str
    categories: List[str]
    abstract: str

    class Config:
        arbitrary_types_allowed = True

class DoUpload(BaseModel):

    file: str
    survey: Optional[bool] = False

class DeleteIDs(BaseModel):

    ids: List[str]

class CreateData(BaseModel):

    papers: List[UploadData]

    