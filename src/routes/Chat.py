from fastapi import APIRouter, Request, status, Form, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Optional
from controllers import NLPController, ChatController
from langchain_core.messages import HumanMessage
from enums import ResponseEnum
from scheme import RenameChat, TemporaryChat

chat_router = APIRouter()

@chat_router.post("/chat/{user_id}/{thread_id}")
async def chat(request:Request, user_id: str, thread_id:str, message: Optional[str] = Form(default=None), 
                      voice: Optional[UploadFile]= File(default=None), image: Optional[UploadFile] = File(default=None)):
    
    nlp_controller = NLPController(db_client= request.app.db_client, generation_client =request.app.generation_client,
                                  template_parser = request.app.template_parser)
    
    chat_controller = ChatController(db_client = request.app.db_client)

    prompt_parts = []
    voice_response_signal = None
    image_response_signal = None
    chat_title = None

    if not message and not voice and not image:
  
        return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content = {
                            "Response_signal": ResponseEnum.NO_INPUT_PROVIDED.value
                            }
                        )
    
    if message:
        prompt_parts.append(message.strip())

    if voice:

        try:
            transcription, voice_response_signal = await nlp_controller.trascribe_audio(
                voice, request.app.audio_client
            )

            if transcription == None:
                return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content = {
                            "Response_signal": voice_response_signal
                            }
                        )
            
            prompt_parts.append(f"Transcription: {transcription}")
        except Exception as e:
            return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content = {
                            "Response_signal": voice_response_signal
                            }
                        )

    if image:

        try:

            image_text, image_response_signal = await nlp_controller.extract_text_from_image(image)

            if image_text == None:
                return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content = {
                            "Response_signal": image_response_signal
                            }
                        )
            
            prompt_parts.append(f"Image Text: {image_text}")

        except Exception as e:
            return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content = {
                            "Response_signal": image_response_signal
                            }
                        )

    prompt = "\n".join(prompt_parts).strip()

    is_chat_exists = await chat_controller.is_chat_exists(thread_id=thread_id, user_id=user_id)

    if not is_chat_exists:
        try:
            chat_title = await nlp_controller.generate_answer(
                service="generate_title",
                input_text=prompt,
            )
        except Exception as e:
            return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content = {
                                "Response_signal": ResponseEnum.GENERATE_TITLE_FAILURE.value
                                }
                            )
    
            
        _ = await chat_controller.save_chat_metadata({
            "thread_id": thread_id,
            "title": chat_title,
            "user_id": user_id
        })

    return StreamingResponse(chat_controller.stream_generator(prompt=prompt, thread_id=thread_id, 
                                         graph=request.app.assistant_graph, chat_title=chat_title), 
                                         media_type="text/event-stream")
    
    

@chat_router.post("/rename/chat")
async def rename_chat_title(request:Request, chat_metadata: RenameChat):

    chat_controller = ChatController(db_client = request.app.db_client)
  

    is_renamed= await chat_controller.rename_chat({
                        "thread_id": chat_metadata.thread_id,
                        "title": chat_metadata.new_title,
                        "user_id": chat_metadata.user_id
                    })
    if is_renamed:
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content = {
                        "Response_signal": ResponseEnum.CHAT_RENAME_SUCCESS.value
                        }
                    )

    return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content = {
                        "Response_signal": ResponseEnum.CHAT_RENAME_FAILURE.value
                        }
                    )

    


@chat_router.delete("/temporary/chat")
async def temporary_chat(request:Request, chat_metadata: TemporaryChat):

    chat_controller = ChatController(db_client = request.app.db_client)
    is_deleted = await chat_controller.delete_chat_by_thread_id(chat_metadata.thread_id)

    if not is_deleted:
        return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content = {
                            "Response_signal": ResponseEnum.CHAT_DELETION_FAILURE.value
                            }
                        )
    
    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content = {
                            "Response_signal": ResponseEnum.CHAT_DELETION_SUCCESS.value
                            }
                        )