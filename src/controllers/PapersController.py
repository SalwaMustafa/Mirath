from scheme import UploadData
from enums import DatabaseEnum, ResponseEnum
import logging
from typing import List
from .NLPController import NLPController


class PapersController:

    def __init__(self, db_client, vector_db_client, embedding_client):
        
        self.db_client = db_client
        self.vector_db_client = vector_db_client
        self.embedding_client = embedding_client
        self.collection = self.db_client[DatabaseEnum.RESEARCH_COLLECTION_NAME.value]

        self.nlp_controller = NLPController(db_client = self.db_client, 
                                            embedding_client = self.embedding_client,
                                            vector_db_client = self.vector_db_client,
                                            survey = False)

        self.logger = logging.getLogger(__name__)


    async def are_papers_exist(self, ids: List[str]) -> dict[str, bool]:
       
        existing_docs = await self.collection.find({"id": {"$in": ids}}).to_list(length=len(ids))
        existing_ids = {doc["id"] for doc in existing_docs}

        return {id : id in existing_ids for id in ids}
    

    async def delete_papers(self, ids: List[str]):
        existing_status = await self.are_papers_exist(ids)
        existing_ids = [id for id, exists in existing_status.items() if exists]
        result_from_qdrant = False

        if existing_ids:

            result_from_mongo = await self.collection.delete_many({"id": {"$in": existing_ids}})
            self.logger.info(f"Deleted {result_from_mongo.deleted_count} papers: {existing_ids}")


            result_from_qdrant = self.vector_db_client.delete_records(
                collection_name = DatabaseEnum.RESEARCH_COLLECTION_NAME.value, 
                ids = existing_ids
                )
            self.logger.info(f"Deleted papers from Qdrant: {existing_ids}")

            not_found_ids = [id for id, exists in existing_status.items() if not exists]
            return result_from_qdrant, not_found_ids, ResponseEnum.PAPER_DELETED_SUCCESSFULLY.value

        self.logger.error(f"No papers found for IDs: {ids}")
        return result_from_qdrant , ids, ResponseEnum.DELETION_FAILURE.value

    
    async def create_papers(self, data_list: List[dict]):
        created_ids = []
        failed = []
        qdrant_data = []

        for data in data_list:
            try:
                validated_data = UploadData(**data)
                doc_dict = validated_data.dict(by_alias=True, exclude_unset=True)

                await self.collection.update_one(
                    {"id": doc_dict["id"]},  
                    {"$set": doc_dict},    
                    upsert=True
                )
                
                created_ids.append(doc_dict.get("id"))
                qdrant_data.append(doc_dict)
            except Exception as e:
                self.logger.error(f"Error while adding paper in mongo database {data.get('id')}: {e}")
                failed.append(data.get("id"))
        
        signal, _ = await self.nlp_controller.index_into_qdrantdb(
            collection_name = DatabaseEnum.RESEARCH_COLLECTION_NAME.value, 
            data = qdrant_data)
      

        return signal, failed, ResponseEnum.DATAUPLOAD_SUCCESS.value if created_ids and signal else ResponseEnum.CREATE_PAPER_FAILURE.value
    


