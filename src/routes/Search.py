from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from scheme import Search
from controllers import NLPController
from enums import DatabaseEnum

search_router = APIRouter()

@search_router.get("/search/papers")
async def search_papers(request: Request, search_request: Search):

    question = search_request.question
    db_client = request.app.db_client

    nlp_controller = NLPController(db_client = db_client)
    response = await nlp_controller.search_into_vector_db(
        collection_name = DatabaseEnum.RESEARCH_COLLECTION_NAME.value, 
        question = question)
    
    return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "response": response
                    }
                )
    
    