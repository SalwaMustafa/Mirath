import asyncio
import os
from enums import DatabaseEnum
from llm.providers import CohereProvider
from helpers.config import get_settings
from llm import DocumentTypeEnum
from vectordb.providers import QdrantProvider
import logging
from enums.ResponseEnum import ResponseEnum

class NLPController:

    def __init__(self,db_client:str, survey:bool=False):
        self.db_client = db_client
        self.collection = (
            self.db_client[DatabaseEnum.SURVEY_COLLECTION_NAME.value]
            if survey
            else self.db_client[DatabaseEnum.RESEARCH_COLLECTION_NAME.value]
        )
        self.settings = get_settings()
        self.cohere_provider = CohereProvider(api_key=self.settings.COHERE_API_KEY)
        self.qdrant_provider =QdrantProvider(qdrant_url=self.settings.QDRANT_URL,
                                             distance=self.settings.DISTANCE_METHOD)
        
        self.logger = logging.getLogger(__name__)

    async def embed_papers(self, page_no:int=1, page_size:int=25):
            records = await (
                self.collection
                .find()
                .skip((page_no - 1) * page_size)
                .limit(page_size)
                .to_list(length=None))

            ids, texts, vectors, metadatas = [], [], [], []

            for record in records:
                embedding_response = self.cohere_provider.embed_text(text = record["abstract"], 
                                                                     document_type = DocumentTypeEnum.DOCUMENT.value)
                
                if embedding_response is None:
                     continue
                
                vectors.extend(embedding_response)
                ids.append(record["id"])
                texts.append(record["abstract"])
                metadatas.append({
                    "title": record["title"],
                    "categories":record["categories"]})
                
            return ids, texts, vectors, metadatas
    
    async def index_into_qdrantdb(self,collection_name:str, do_reset:bool=False):
        ids, texts, vectors, metadatas = await self.embed_papers()

        _= self.qdrant_provider.create_collection(
             collection_name=collection_name,
             embedding_size=self.settings.EMBEDDING_MODEL_SIZE,
             do_reset=do_reset
        )

        signal = await asyncio.to_thread(
              self.qdrant_provider.insert_many(
              collection_name=collection_name,
              texts=texts,
              vectors=vectors,
              metadatas=metadatas,
              record_ids=ids
              ))
        
        if not signal:
            self.logger.error("Error inserting data into Qdrant vector database.")
            return ResponseEnum.VECTOR_DB_INSERTION_ERROR.value
        
        return ResponseEnum.VECTOR_DB_INSERTION_SUCCESS.value
         
         
         
    

    
                
             
                


                 
                


        


       