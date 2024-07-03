from pydantic import BaseModel
from fastapi import UploadFile

class HTTPRequest(BaseModel):
    status_code: int
    message: str

class ChatEngineSettings(BaseModel):
    model_name: str
    llm_temperature: float
    embedding_model: str
    file: UploadFile
    web_url: str

    class Config:
        arbitrary_types_allowed = True