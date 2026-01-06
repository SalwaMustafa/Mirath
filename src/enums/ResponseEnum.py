from enum import Enum

class ResponseEnum(Enum):

    DATAUPLOAD_SUCCESS = "Data uploaded successfully."
    DATAUPLOAD_FAILURE = "Data upload completed with some errors."
    INVALID_FILE_FORMAT = "Unsupported file format."
    VECTOR_DB_INSERTION_ERROR = "Error inserting data into vector database."
    VECTOR_DB_INSERTION_SUCCESS = "Data inserted into vector database successfully."

    