from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routes import healthy_check_router, upload_data_router
from llm.LLMProviderFactory import LLMProviderFactory
from helpers.config import get_settings
from vectordb.VectorDBFactory import VectorDBFactory
app = FastAPI()

@app.on_event("startup")
async def startup_app():

    settings = get_settings()
    llm_provider_factory = LLMProviderFactory(config = settings)
    
    app.mongo_conn = AsyncIOMotorClient(settings.CONNECTION_URL)
    app.db_client = app.mongo_conn[settings.DATABASE_NAME]

    app.embedding_client = llm_provider_factory.get_llm(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(
        model_id = settings.EMBEDDING_MODEL_ID ,
        embedding_size = settings.EMBEDDING_MODEL_SIZE 
    )

    vector_db_factory = VectorDBFactory(config = settings)
    app.vector_db_client = vector_db_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vector_db_client.connect()


@app.on_event("shutdown")
async def shutdown_app():
    app.mongo_conn.close()
    app.vector_db_client.disconnect()


app.include_router(healthy_check_router)
app.include_router(upload_data_router)