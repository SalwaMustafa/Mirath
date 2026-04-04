from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from scheme import AIServices
from controllers import NLPController
from enums import ResponseEnum


ai_services_router = APIRouter() 

@ai_services_router.post("/AI/Services")
async def ai_services(request: Request, user_request: AIServices):
    
    service = user_request.service
    input_text = user_request.input_text
    target_language = user_request.target_language

    nlp_controller = NLPController(
        db_client = request.app.db_client,
        generation_client = request.app.generation_client,
        template_parser = request.app.template_parser
        )

    answer = await nlp_controller.generate_answer(
        service=service,
        input_text=input_text,
        target_language=target_language
    )


    if answer:
        return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={
                            "answer": answer
                        }
                    )
    else:
        return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "answer": ResponseEnum.GENERATION_FAILURE.value
                        }
                    )
    
    



