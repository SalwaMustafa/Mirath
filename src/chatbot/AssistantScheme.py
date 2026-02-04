from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from typing import Annotated, List, Literal, TypedDict, Optional
import operator


class UserProfile(BaseModel):
    """
    Long-Term Memory: Stores user attributes that persist across sessions.

    """
    name: str = Field(description="User's name", default="Researcher")
    research_level: Optional[Literal["Undergraduate","Master's Student","PhD Researcher","Professor"]] = Field(description="User's expertise level", default = None)
    field_of_interest: Optional[str] = Field(description="Main research field (e.g., NLP, Computer Vision)", default = None)
    preferred_language: Literal["English", "Arabic"] = Field(description="User's preferred language", default = "English")
    notable_publications: Optional[List[str]] = Field(description="List of user's notable publications", default = None)


class RoadmapRequirements(BaseModel):
    """
    Specific requirements for the current roadmap request.

    """
    topic: Optional[str] = Field(description="The specific research topic", default = None)
    time_frame: Optional[str] = Field(description="Available time", default = None)


class ExtractionSchema(BaseModel):
    """
    Schema for extracting information from user messages
    
    """
    name: Optional[str] = Field(description="User's name if mentioned", default=None)
    topic: Optional[str] = Field(description="Research topic", default=None)
    time_frame: Optional[str] = Field(description="Time frame", default=None)
    research_level: Optional[Literal["Undergraduate", "Master's Student", "PhD Researcher", "Professor"]] = Field(
        description="Research level", 
        default=None
    )
    field_of_interest: Optional[str] = Field(description="Field of interest", default=None)
    preferred_language: Optional[Literal["English", "Arabic"]] = Field(
        description="Preferred language", 
        default="English"
    ) 
    notable_publications: Optional[List[str]] = Field(description="List of user's notable publications", default = None)


class RouteQuery(BaseModel):
    destination: Literal["general_assistant", "roadmap_guardian"] = Field(
        ..., description = "Select 'roadmap_guardian' ONLY if the user explicitly asks for a study plan, learning path, or roadmap. Otherwise 'general_assistant'."
    )


class EvaluationResult(BaseModel):
    is_satisfactory: Literal["PASS", "FAIL"] = Field(description="PASS if answer is accurate, detailed, and contains CITATIONS.")
    reasoning: str = Field(description="Brief explanation of the evaluation of why you made this decision.")
    feedback: str = Field(description="Feedback needed to fix the answer.")


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_profile: UserProfile
    roadmap_reqs: RoadmapRequirements 
    next_step: str
    reflexion_count: int
    agent_type: str
