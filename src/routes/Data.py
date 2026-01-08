from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from controllers import UploadDataController, PapersController
from scheme import DoUpload, DeleteIDs, CreateData
from enums import ResponseEnum



data_router = APIRouter() 

@data_router.post("/upload/papers")
async def upload_researches(request: Request, do_upload: DoUpload):
    
    db_client = request.app.db_client
    embedding_client = request.app.embedding_client
    vector_db_client = request.app.vector_db_client
    file =  do_upload.file
    survey = do_upload.survey

    upload_data_controller = UploadDataController(
        file = file, 
        db_client = db_client, 
        cohere_provider=embedding_client, 
        qdrant_provider=vector_db_client, 
        survey = survey
        )

    counter, message_from_mongo, message_from_qdrant  = await upload_data_controller.upload_data()

    if counter==0 :
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message from mongo": message_from_mongo,
                        "message from qdrant": message_from_qdrant
                    }
                )
    else:
         return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message from mongo": message_from_mongo,
                        "message from qdrant": message_from_qdrant
                    }
                )
    

@data_router.delete("/papers")
async def delete_researches(request: Request, ids_to_delete: DeleteIDs):

    db_client = request.app.db_client
    embedding_client = request.app.embedding_client
    vector_db_client = request.app.vector_db_client
    papers_controller = PapersController(
        db_client = db_client,
        vector_db_client = vector_db_client,
        embedding_client = embedding_client
        )

    result_from_qdrant, not_found_ids, message = await papers_controller.delete_papers(
        ids=ids_to_delete.ids
    )

    if not result_from_qdrant and not_found_ids:
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_200_OK

    return JSONResponse(
        status_code=status_code,
        content={
            "result from qdrant": (
                ResponseEnum.PAPER_DELETED_SUCCESSFULLY.value 
                if result_from_qdrant 
                else ResponseEnum.DELETION_FAILURE.value
                ),
            "result from mongo": message,
            "not_found": not_found_ids, 
        }
    )



@data_router.post("/create/papers")
async def create_researches(request: Request, papers_to_create: CreateData):

    db_client = request.app.db_client
    embedding_client = request.app.embedding_client
    vector_db_client = request.app.vector_db_client
    papers = papers_to_create.papers
    papers_controller = PapersController(
        db_client = db_client,
        vector_db_client = vector_db_client,
        embedding_client = embedding_client
        )


    result_from_qdrant, failed_ids, message = await papers_controller.create_papers(
        data_list=papers
    )

    status_code = (
        status.HTTP_201_CREATED
        if result_from_qdrant and not failed_ids
        else status.HTTP_404_NOT_FOUND
    )

    return JSONResponse(
        status_code=status_code,
        content={
           "result from qdrant": (
                ResponseEnum.DATAUPLOAD_SUCCESS.value 
                if result_from_qdrant 
                else ResponseEnum.CREATE_PAPER_FAILURE.value
                ),
            "result from mongo": message,
            "failed ids": failed_ids,
        }
    )
