from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional, List

class HTTPRequest(BaseModel):
    status_code: int
    message: str

class ChatEngineSettings(BaseModel):
    model: str
    llm_temperature: float
    embedding_model: str
    web_url: Optional[List[str]] = None
    file: Optional[UploadFile] = None

    class Config:
        arbitrary_types_allowed = True