from pydantic import BaseModel, Field
from typing import Optional, List
from bson.objectid import ObjectId


class RenameChat(BaseModel):

    thread_id: str
    new_title: str
    user_id: str



class TemporaryChat(BaseModel):

    thread_id: str
