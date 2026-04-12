import logging
from enums import DatabaseEnum
from scheme import SaveChatMetadata
from datetime import datetime

class ChatController:
    def __init__(self, db_client):
        self.db_client = db_client
        self.chat_metadata_collection = self.db_client[DatabaseEnum.CHAT_METADATA_COLLECTION_NAME.value]
        self.logger = logging.getLogger(__name__)

    async def save_chat_metadata(self, metadata: dict):
        try:
            metadata = SaveChatMetadata(**metadata)

        except Exception as e:
                self.logger.error(f"Error while validate data: {e}")
                return False
    
        metadata_dict = metadata.dict(by_alias=True, exclude_unset=True)
        await self.chat_metadata_collection.update_one(
            {"thread_id": metadata_dict["thread_id"]},
            {"$set": {"title": metadata_dict["title"], 
                      "created_at": datetime.utcnow()}},
            upsert=True
        )
        return True

    async def delete_chat_by_thread_id(self, thread_id:str):

        chat_history = self.db_client[DatabaseEnum.CHAT_HISTORY_COLLECTION_NAME.value]
        is_exist = await chat_history.find_one({"thread_id": thread_id})

        if not is_exist:
            self.logger.warning(f"Thread ID {thread_id} does not exist in chat history.")
            return False

        checkpoint_writes_collection = self.db_client[DatabaseEnum.CHECKPOINT_WRITES.value]
        
        await checkpoint_writes_collection.delete_many({"thread_id": thread_id})
        await chat_history.delete_many({"thread_id": thread_id})
        await self.chat_metadata_collection.delete_one({"thread_id": thread_id})

        return True

