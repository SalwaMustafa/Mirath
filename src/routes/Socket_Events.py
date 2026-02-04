import socketio
from helpers.config import get_settings
from scheme import InitUserData, GenerateRequest
from langchain_core.messages import HumanMessage


settings = get_settings()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
def init_socket(app):
    app.mount("/", socketio.ASGIApp(sio, app))
    
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