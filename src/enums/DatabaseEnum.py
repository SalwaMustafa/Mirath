from enum import Enum

class DatabaseEnum(Enum):

    RESEARCH_COLLECTION_NAME = "ResearchPapers"
    SURVEY_COLLECTION_NAME = "SurveyPapers"
    CHAT_HISTORY_COLLECTION_NAME = "chat_history"
    CHAT_METADATA_COLLECTION_NAME = "chat_metadata"
    CHECKPOINT_WRITES = "checkpoint_writes"
    