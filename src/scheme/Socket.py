from pydantic import BaseModel, Field

class InitUserData(BaseModel):
    user_id: str = Field(...)
    thread_id: str =Field(...)

class GenerateRequest(BaseModel):
    message: str = Field(...)
    