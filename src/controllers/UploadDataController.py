from scheme import UploadData
from enums import FileExtensionEnum, DatabaseEnum, ResponseEnum
import aiofiles
import os
import json
import logging
class UploadDataController():

    def __init__(self, file, db_client, survey = False):

        self.base_dir = os.path.dirname( os.path.dirname(__file__) )
        self.file_path = os.path.join(self.base_dir, "assets", "data" , file)
        self.db_client = db_client

        if survey:
            self.collection = self.db_client[DatabaseEnum.SURVEY_COLLECTION_NAME.value]
        else:
            self.collection = self.db_client[DatabaseEnum.RESEARCH_COLLECTION_NAME.value]

        self.counter = 0
        self.logger = logging.getLogger(__name__)

    def get_file_extension(self):

        return os.path.splitext(self.file_path)[1].lower()
    
    async def upload_data(self):

        extension = self.get_file_extension()

        if extension == FileExtensionEnum.JSONL.value:

            async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                async for line in f:
                    try:
                        data = json.loads(line)
                        validated_data = UploadData(**data)
                        await self.collection.insert_one(validated_data.dict(by_alias=True, exclude_unset=True))
                    except Exception as e:
                        self.counter +=1
                        self.logger.error(f"Error while inserting data: {e}")
                    

            if self.counter == 0:
                return self.counter , ResponseEnum.DATAUPLOAD_SUCCESS.value
            
            else:
                return self.counter , ResponseEnum.DATAUPLOAD_FAILURE.value
            
        return 0, ResponseEnum.INVALID_FILE_FORMAT.value


