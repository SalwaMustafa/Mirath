from enum import Enum

class ResponseEnum(Enum):

    DATAUPLOAD_SUCCESS = "Data uploaded successfully."
    DATAUPLOAD_FAILURE = "Data upload completed with some errors."
    INVALID_FILE_FORMAT = "Unsupported file format."
    