from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "Qdrant"
    QDRANT_COLLECTION_FOR_SEARCH = "qdrant_collection_for_search"
    

class Distance(Enum):
    COSINE = "Cosine"
    DOT = "Dot"