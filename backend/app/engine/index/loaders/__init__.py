from typing import Optional, List
from fastapi import UploadFile
from .file import get_file_documents
from .web import get_web_documents

def load_documents(file: Optional[UploadFile] = None, web_links: Optional[List[str]] = None):
    documents = []

    if file is not None:
        document = get_file_documents(file)
        documents.extend(document)

    if web_links:
        documents.extend(get_web_documents(web_links))

    return documents