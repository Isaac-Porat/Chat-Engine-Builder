import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import HTTPRequest, ChatEngineSettings
from engine.settings import init_settings
from engine.index.generate_index import generate_datasource

app = FastAPI()

logger = logging.getLogger("uvicorn")


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

app.get('/')
async def index():
    return {"message": "hello world!"}

app.get('/chat-engine-settings')
async def engine_settings(data: ChatEngineSettings):
    try:

        model = data.model_name
        llm_temp = data.llm_temperature
        embedding_model = data.embedding_model

        init_settings(model, llm_temp, embedding_model)

        file = data.file
        web_url = data.web_url

        generate_datasource(file, web_url)

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


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)