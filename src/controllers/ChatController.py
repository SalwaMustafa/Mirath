import logging
from enums import DatabaseEnum
from scheme import SaveChatMetadata
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
import json
from enums import ResponseEnum
from helpers import STREAM_CONFIG

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

        await self.chat_metadata_collection.insert_one({
                        "thread_id": metadata_dict["thread_id"], 
                        "user_id": metadata_dict["user_id"],
                        "title": metadata_dict["title"],
                        "created_at": datetime.utcnow()})

        return True
    
    async def rename_chat(self, metadata: dict):
        try:
            metadata = SaveChatMetadata(**metadata)

        except Exception as e:
                self.logger.error(f"Error while validate data: {e}")
                return False
    
        metadata_dict = metadata.dict(by_alias=True, exclude_unset=True)

        if await self.is_chat_exists(thread_id=metadata_dict["thread_id"], user_id=metadata_dict["user_id"]):
            await self.chat_metadata_collection.update_one(
            {"thread_id": metadata_dict["thread_id"], "user_id": metadata_dict["user_id"]},
            {"$set": {"title": metadata_dict["title"]}}
            )
            return True
        return False

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

    async def is_chat_exists(self, thread_id: str, user_id: str):

        is_exist = await self.chat_metadata_collection.find_one({"thread_id": thread_id, "user_id": user_id})
        if is_exist:
            return True
        return False
    

    
    async def stream_generator(self, prompt: str, thread_id: str, graph, chat_title: str = None):
        if chat_title:
                yield f"data: {json.dumps({
                    'type': 'chat_title',
                    'content': chat_title
                })}\n\n"

        config = {"configurable": {"thread_id": thread_id}}        
        final_response = ""

        try:

            async for chunk in graph.astream(
                {
                    "messages": [
                        HumanMessage(
                            content=prompt,
                            additional_kwargs={"type": "user_query"},
                        )
                    ]
                },
                config=config,
                stream_mode="updates"
            ):
                
                for node_name, state_update in chunk.items():
                    
                    if node_name in STREAM_CONFIG:
                        yield f"data: {json.dumps({
                            'type': 'status',
                            'content': STREAM_CONFIG[node_name]
                        })}\n\n"
                    
                    if "messages" in state_update and state_update["messages"]:
                        last_message = state_update["messages"][-1]
                        
                        if isinstance(last_message, AIMessage) and last_message.content:
                            final_response = last_message.content

            if final_response:

                yield f"data: {json.dumps({
                    'type': 'model_answer',
                    'content': final_response
                })}\n\n"

            yield f"data: {json.dumps({
                'type': 'end',
                'content': ResponseEnum.STREAMING_SUCCESS.value 
            })}\n\n"

            
        except Exception as e:
            self.logger.error(f"Error during streaming: {e}")
            
            yield f"data: {json.dumps({
                'type': 'error',
                'content': ResponseEnum.STREAMING_FAILURE.value
            })}\n\n"
        
        