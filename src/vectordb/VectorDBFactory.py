from .providers import QdrantProvider
from .VectorDBEnum import VectorDBEnum
from controllers import BaseController

class VectorDBFactory:

    def __init__(self, config:str):
        self.config = config
        self.base_controller = BaseController()


    def create(self, provider:str):

        qdrant_path = self.base_controller.get_database_path("qdrant_data")

        if provider == VectorDBEnum.QDRANT.value:
            
            return QdrantProvider(
            qdrant_url=self.config.QDRANT_URL,
            qdrant_path=qdrant_path,
            distance=self.config.DISTANCE_METHOD
        )

