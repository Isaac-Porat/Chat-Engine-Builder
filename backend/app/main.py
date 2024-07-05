import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import HTTPRequest, ChatEngineSettings
from engine.settings import set_settings
from engine.index.generate_index import generate_datasource
from engine.api.routers.chat import chat_router
from engine.index.index import get_index

app = FastAPI()

logger = logging.getLogger("uvicorn")

app.include_router(chat_router, prefix="/api/chat")

environment = "dev"
if environment == "dev":
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get('/')
async def index():
    return {"message": "hello world!"}

@app.post('/chat-engine-settings')
async def engine_settings(data: ChatEngineSettings):
    try:

        model = data.model
        llm_temp = data.llm_temperature
        embedding_model = data.embedding_model

        set_settings(model, llm_temp, embedding_model)

        web_urls = data.web_url
        file = data.file

        generate_datasource(file, web_urls)

        return HTTPRequest(
            status_code=201,
            message="Chat engine settings initialized successfully"
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error getting chat engine settings {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=f"Error getting chat engine settings {str(e)}"
        )

@app.get('/get-index')
async def get_current_index():
    index = get_index()

    if not index:
        return HTTPException(
            status_code=404,
            detail="Index not found"
        )

    return HTTPRequest(
        status_code=200,
        message="Index found"
    )

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)