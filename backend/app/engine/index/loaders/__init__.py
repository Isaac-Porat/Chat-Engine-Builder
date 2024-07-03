from typing import Optional, List
from fastapi import UploadFile
from loaders.web import WebLoaderConfig, get_web_documents
from loaders.file import get_file_documents

def load_documents(file: Optional[UploadFile] = None, web_links: Optional[List[str]] = None):
    documents = []

    if file is not None:
        document = get_file_documents(file)
        documents.extend(document)

    if web_links:
        documents.extend(get_web_documents(web_links))

    return documents