from scheme import UploadData
from enums import FileExtensionEnum, DatabaseEnum, ResponseEnum
import aiofiles
import os
import json
import logging
from .NLPController import NLPController


class UploadDataController:

    def __init__(self, file, db_client, vector_db_client, embedding_client, survey=False):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_path = os.path.join(self.base_dir, "assets", "data", file)
        self.db_client = db_client
        self.survey = survey
        self.embedding_client = embedding_client
        self.vector_db_client = vector_db_client
        self.nlp_controller = NLPController(
            db_client=self.db_client,
            embedding_client=self.embedding_client,
            vector_db_client=self.vector_db_client,
            survey=self.survey
        )

        self.mongo_collection = (
            self.db_client[DatabaseEnum.SURVEY_COLLECTION_NAME.value]
            if self.survey
            else self.db_client[DatabaseEnum.RESEARCH_COLLECTION_NAME.value]
        )

        self.qdrant_collection_name = (
            DatabaseEnum.SURVEY_COLLECTION_NAME.value
            if self.survey
            else DatabaseEnum.RESEARCH_COLLECTION_NAME.value
        )

        self.logger = logging.getLogger(__name__)
        self.failed_records = 0

    def get_file_extension(self):
        return os.path.splitext(self.file_path)[1].lower()


    async def load_and_validate_file(self) -> list[dict]:
        validated_records = []

        extension = self.get_file_extension()

        try:
            if extension == FileExtensionEnum.JSONL.value:
                async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                    async for line in f:
                        try:
                            record = UploadData(**json.loads(line))
                            validated_records.append(
                                record.dict(by_alias=True, exclude_unset=True)
                            )
                        except Exception as e:
                            self.failed_records += 1
                            self.logger.error(f"Validation error: {e}")

            elif extension == FileExtensionEnum.JSON.value:
                async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                    data_list = json.loads(await f.read())

                    for item in data_list:
                        try:
                            record = UploadData(**item)
                            validated_records.append(
                                record.dict(by_alias=True, exclude_unset=True)
                            )
                        except Exception as e:
                            self.failed_records += 1
                            self.logger.error(f"Validation error: {e}")

            else:
                raise ValueError(ResponseEnum.INVALID_FILE_FORMAT.value)

        except Exception as e:
            self.logger.error(f"File parsing failed: {e}")
            raise

        return validated_records

  
    async def upload_data(self):

        try:
            validated_data = await self.load_and_validate_file()

            if validated_data == []:
                self.logger.error("No valid data to upload")
                return self.failed_records, ResponseEnum.DATAUPLOAD_FAILURE.value, None
            
            signal, message = await self.nlp_controller.index_into_qdrantdb(
                collection_name=self.qdrant_collection_name,
                data=validated_data
            )

            if not signal:
                self.logger.error("Indexing into Qdrant failed")
                return self.failed_records, ResponseEnum.DATAUPLOAD_FAILURE.value, message

            await self.mongo_collection.insert_many(validated_data)

            return self.failed_records, ResponseEnum.DATAUPLOAD_SUCCESS.value, message

        except Exception as e:
            self.logger.error(f"Upload pipeline failed: {e}")
            return self.failed_records, ResponseEnum.DATAUPLOAD_FAILURE.value, None

