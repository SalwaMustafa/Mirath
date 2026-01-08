from VectorDBInterface import VectorDBInterface
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointIdsList
from VectorDBEnum import Distance
import logging
from typing import List


class QdrantProvider(VectorDBInterface):

    def __init__(self, qdrant_url:str,distance):
        
        self.qdrant_url = qdrant_url
        self.qdrant_client = None
        if distance == Distance.COSINE.value:
            self.distance = models.Distance.COSINE
        elif distance == Distance.DOT.value:
            self.distance = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.qdrant_client = QdrantClient(url=self.qdrant_url)

    def disconnect(self):
        self.qdrant_client = None

    def is_collection_exists(self, collection_name:str)-> bool:
       return self.qdrant_client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self)->List:
        return self.qdrant_client.get_collections()
    
    def get_collection_info(self,collection_name:str)->dict:
        return self.qdrant_client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name:str)->bool:
        if self.is_collection_exists(collection_name):
            _ = self.qdrant_client.delete_collection(collection_name=collection_name)
            return True
        
        self.logger.error(f"Collection {collection_name} does not exist.")
        return False
    
    def delete_records(self, collection_name:str, ids: List[str])->bool:
        if self.is_collection_exists(collection_name):
            _ = self.qdrant_client.delete(
                collection_name=collection_name,
                points_selector=PointIdsList(points = ids)
                )
            return True
        
        self.logger.error(f"Collection {collection_name} does not exist.")
        return False
    
    def create_collection(self, collection_name:str, embedding_size:int, do_reset:bool=False):
        if do_reset and self.is_collection_exists(collection_name):
            self.delete_collection(collection_name=collection_name)

        if not self.is_collection_exists(collection_name):
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=embedding_size, distance=self.distance))
            return True
        
        self.logger.error(f"Collection {collection_name} already exists.")
        return False
    
    def insert_one(self, collection_name:str, text:str, vector:list, metadata:dict=None, record_id:str=None):
        if self.is_collection_exists(collection_name=collection_name):
            try:
                self.qdrant_client.upload_points(
                    collection_name=collection_name,
                    points=[models.PointStruct(id=record_id, vector=vector,
                                            payload={"metadata":metadata, "text":text})])
                return True
            except Exception as e:
                self.logger.error(f"Error inserting point: {e}")
                return False
        
        self.logger.error(f"Collection {collection_name} does not exist.")
        return False

    def insert_many(self, collection_name:str, texts:list, vectors:list, metadatas:list=None,
                     record_ids:list=None,batch_size:int=25):
        if self.is_collection_exists(collection_name=collection_name):

            try:
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i:i+batch_size]
                    batch_vectors = vectors[i:i+batch_size]
                    batch_metadatas = metadatas[i:i+batch_size] if metadatas else [None]*len(batch_texts)
                    batch_record_ids = record_ids[i:i+batch_size] if record_ids else [None]*len(batch_texts)

                    points = [
                        models.PointStruct(
                            id=batch_record_ids[j],
                            vector=batch_vectors[j],
                            payload={
                                "text": batch_texts[j],
                                "metadata": batch_metadatas[j]
                            }
                        )
                        for j in range(len(batch_texts))
                    ]

                    self.qdrant_client.upload_points(
                        collection_name=collection_name,
                        points=points
                    )

                return True

            except Exception as e:
                self.logger.error(f"Error inserting points: {e}")
                return False
            
        self.logger.error(f"Collection {collection_name} does not exist.")
        return False
    
    def search_by_vector(self, collection_name:str, vector:list, limit:int=5):
        return self.qdrant_client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit)
