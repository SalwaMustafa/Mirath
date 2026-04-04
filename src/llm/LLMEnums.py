from enum import Enum

class CohereEnums(Enum):

    DOCUMENT = "search_document"
    QUERY = "search_query"
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "chatbot"

class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"

class LLMEnums(Enum):
    GEMINI = "GEMINI"
    COHERE = "COHERE"

class GeminiEnums(Enum):

    DOCUMENT = "RETRIEVAL_DOCUMENT"
    QUERY = "RETREIVAL_QUERY"
