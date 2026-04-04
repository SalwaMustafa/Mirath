from enum import Enum

class ResponseEnum(Enum):

    DATAUPLOAD_SUCCESS = "Data uploaded successfully."
    DATAUPLOAD_FAILURE = "Unable to upload some records."
    INVALID_FILE_FORMAT = "Unsupported file format."
    VECTOR_DB_INSERTION_ERROR = "Error inserting data into vector database."
    VECTOR_DB_INSERTION_SUCCESS = "Data inserted into vector database successfully."
    PAPER_DELETED_SUCCESSFULLY = "Paper deleted successfully."
    DELETION_FAILURE = "Cannot delete paper because this ID is not in the database."
    CREATE_PAPER_FAILURE = "Failed to create papers"
    ID_NOT_FOUND = "ID not found"
    PAPER_NOT_FOUND = "Paper not found"
    PAPER_UPDATED_SUCCESSFULLY = "Paper updated successfully"
    NO_CHANGES_MADE = "No changes were made"
    PAPER_UPDATE_FAILURE = "Cannot update this paper"
    CANNOT_EMBED_TEXT = "Cannot embed the provided text."  
    GENERATION_FAILURE = "Failed to generate a response."
