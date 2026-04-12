import socketio
from helpers.config import get_settings
from scheme import InitUserData, GenerateRequest
from langchain_core.messages import HumanMessage
from controllers import NLPController, ChatController


settings = get_settings()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio)

def init_socket(app):
    
    @sio.on("init_user")
    async def init_user(sid, data = {} ):
        """
        data = {"user_id": "123",
                "thread_id" : "5642"}
        """
        try:

            user_info = InitUserData(**data) 

            session_data = {
                "user_id": user_info.user_id,
                "thread_id": user_info.thread_id,
                "num_of_messages":0
            }

            await sio.save_session(sid, session_data)
            await sio.emit("ack", {"msg": "User info received"}, to=sid)

        except Exception as e:
            await sio.emit("error", {"msg": f"Init failed: {str(e)}"}, to=sid)

    @sio.on("generate_request")
    async def handle_generate(sid, data = {}):
        """
        data = {"message": "Hello, world!"}
        """


        try:

            content = GenerateRequest(**data)
            if not content.message:
                await sio.emit("error", {"msg": "No message received"}, to=sid)
                return
    
            session = await sio.get_session(sid)
            user_id = session["user_id"]
            thread_id = session["thread_id"]
            session["num_of_messages"] = session["num_of_messages"]+1

            if session["num_of_messages"]==1:
                    nlp_controller = NLPController(
                    db_client = app.db_client,
                    generation_client = app.generation_client,
                    template_parser = app.template_parser
                    )

                    chat_title = await nlp_controller.generate_answer(
                        service = "generate_title",
                        input_text = content.message,
                    )
                    chat_controller = ChatController(app.db_client)
                    _ = await chat_controller.save_chat_metadata({
                        "thread_id": thread_id,
                        "title": chat_title
                    })

                    await sio.emit("chat_title", {"chat_title": chat_title}, to=sid)

            await sio.emit("bot_typing", {
                            "is_typing": True,
                            "status": "thinking",    
                            "action": "Mirath is analyzing your request..."}, to=sid)


            config = {"configurable": {"thread_id": thread_id}}
            result = await app.assistant_graph.ainvoke(
                            {
                                "messages": [HumanMessage(content=content.message,
                                                        additional_kwargs={"type": "user_query"} )]
                                
                            },
                            config=config,
            )
            await sio.emit("bot_typing", {"is_typing": False}, to=sid)
            msg = result["messages"][-1].content
            await sio.emit("bot_message", {"content": msg}, to=sid)
      
            await sio.save_session(sid, session)

        except Exception as e:
           await sio.emit("bot_typing", {"is_typing": False}, to=sid)
           await sio.emit("error", {"msg": "Something went wrong"}, to=sid)

    @sio.on("rename_chat")
    async def rename_chat(sid, data = {}):
        """
        data = {"title": "New Chat Title",
                "thread_id": "5642"}
        """
        try:
            thread_id = data["thread_id"]
            new_title = data["title"]
            
            chat_controller = ChatController(app.db_client)
            _= await chat_controller.save_chat_metadata({
                        "thread_id": thread_id,
                        "title": new_title
                    })
            
            await sio.emit("ack", {"msg": "Chat renamed successfully"}, to=sid)

        except Exception as e:
           await sio.emit("error", {"msg": f"Renaming failed: {str(e)}"}, to=sid)


    @sio.on("temporary_chat")
    async def temporary_chat(sid, data = {}):

        session = await sio.get_session(sid)
        thread_id = session.get("thread_id", "111")
        chat_controller = ChatController(app.db_client)

        is_deleted = await chat_controller.delete_chat_by_thread_id(thread_id)
        if is_deleted:
            await sio.emit("ack", {"msg": "Chat deleted successfully"}, to=sid)
        else:
            await sio.emit("error", {"msg": "Chat deletion failed"}, to=sid)
