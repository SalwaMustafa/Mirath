from .providers import QdrantProvider
from .VectorDBEnum import VectorDBEnum

class VectorDBFactory:

    def __init__(self, config:str):
        self.cofig = config

    def create(self, provider:str):
        if provider == VectorDBEnum.QDRANT.value:
            return QdrantProvider(
                qdrant_url=self.cofig.QDRANT_URL,
                distance=self.cofig.DISTANCE_METHOD
            )
