import asyncio
import os
from enums import DatabaseEnum
from helpers.config import get_settings
from llm import DocumentTypeEnum
import logging
from enums.ResponseEnum import ResponseEnum
from typing import List
from scheme import UploadData
import json
from helpers import SERVICE_CONFIG

class NLPController:

    def __init__(self,db_client:str , vector_db_client = None, embedding_client = None, 
                 generation_client = None, template_parser = None, survey:bool=False):
        
        self.db_client = db_client
        self.collection = (
            self.db_client[DatabaseEnum.SURVEY_COLLECTION_NAME.value]
            if survey
            else self.db_client[DatabaseEnum.RESEARCH_COLLECTION_NAME.value]
        )
        self.settings = get_settings()
        self.vector_db_client = vector_db_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        self.template_parser = template_parser
        
        self.logger = logging.getLogger(__name__)

    async def embed_papers(self, data: List[dict], batch_size: int = 25):
        
        ids, texts, vectors, metadatas = [], [], [], []
        validated_data = []
        for record in data:
            try:
                record = UploadData(**record)
                validated_data.append(record.dict(by_alias=True, exclude_unset=True))

            except Exception as e:
                self.logger.error(f"Error while validate data: {e}")

            
        all_abstracts = [record["abstract"] for record in validated_data]
        all_ids = [record["id"] for record in validated_data]
        all_metadatas = [{"title": record["title"], "categories": record["categories"]} for record in validated_data]

        for i in range(0, len(all_abstracts), batch_size):
            batch_texts = all_abstracts[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]
            batch_metadatas = all_metadatas[i:i+batch_size]

            embedding_response = self.embedding_client.embed_text(
                texts=batch_texts,
                document_type=DocumentTypeEnum.DOCUMENT.value
            )

            if embedding_response is None:
                continue  

            vectors.extend(embedding_response)
            ids.extend(batch_ids)
            texts.extend(batch_texts)
            metadatas.extend(batch_metadatas)

        return ids, texts, vectors, metadatas

    
    async def index_into_qdrantdb(self,collection_name: str, data: List[dict], do_reset: bool = False):
        ids, texts, vectors, metadatas = await self.embed_papers(data = data)

        _= self.vector_db_client.create_collection(
             collection_name=collection_name,
             embedding_size=self.settings.EMBEDDING_MODEL_SIZE,
             do_reset=do_reset
        )

        signal = self.vector_db_client.insert_many(
              collection_name = collection_name,
              texts = texts,
              vectors = vectors,
              metadatas = metadatas,
              record_ids = ids
              )
        
        if not signal:
            self.logger.error("Error inserting data into Qdrant vector database.")
            return False, ResponseEnum.VECTOR_DB_INSERTION_ERROR.value
        
        return True, ResponseEnum.VECTOR_DB_INSERTION_SUCCESS.value
         
         
    
    async def search_into_vector_db(self, collection_name: str, question: str, limit: int = 5):

        embedding_response = self.embedding_client.embed_text(
                texts=[question],
                document_type=DocumentTypeEnum.QUERY.value
            )
        if embedding_response is None:
            return None

        answers = self.vector_db_client.search_by_vector(
            collection_name = collection_name, 
            vector = embedding_response[0], 
            limit = limit
            )

        answers =  json.loads(json.dumps(answers, default = lambda o: o.__dict__))

        return [answers["points"][i]["id"] for i in range(len(answers["points"]))]
    


    async def generate_answer(self, service: str, input_text: str, target_language: str = None):

        config = SERVICE_CONFIG.get(service)
        key = None
        system_vars = {}

        if config:
            key = config["key"]
            system_vars = config["vars"](input_text, target_language)
        else:
            self.logger.error(f"Invalid service: {service}")
            return None
         
        prompt = self.template_parser.get(service , key, system_vars)

        answer = self.generation_client.generate_text(
            prompt = prompt
        )

        return answer
