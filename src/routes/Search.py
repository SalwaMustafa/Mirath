from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from scheme import Search
from controllers import NLPController
from enums import DatabaseEnum
from enums.ResponseEnum import ResponseEnum

search_router = APIRouter()

@search_router.post("/search/papers")
async def search_papers(request: Request, search_request: Search):

    question = search_request.question
    limit = search_request.limit
    db_client = request.app.db_client
    embedding_client = request.app.embedding_client
    vector_db_client = request.app.vector_db_client

    nlp_controller = NLPController( db_client = db_client,
        vector_db_client = vector_db_client,
        embedding_client = embedding_client
        )
    response = await nlp_controller.search_into_vector_db(
        collection_name = DatabaseEnum.RESEARCH_COLLECTION_NAME.value, 
        question = question,
        limit = limit)
    if response:
        return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={
                            "response": response
                        }
                    )
    else:
        return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "response": ResponseEnum.CANNOT_EMBED_TEXT.value
                        }
                    )
    
    