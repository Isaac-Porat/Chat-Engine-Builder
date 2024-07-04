import os
import logging
from dotenv import load_dotenv
from typing import List, Optional

from fastapi import UploadFile
from llama_index.core.settings import Settings
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage import StorageContext

from engine.settings import init_settings
from ..index.loaders import load_documents
from ..index.vectordb import get_vector_store

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

STORAGE_DIR = "storage"

def get_doc_store():
    if os.path.exists(STORAGE_DIR):
        return SimpleDocumentStore.from_persist_dir(STORAGE_DIR)
    else:
        return SimpleDocumentStore()

def run_pipeline(docstore, vector_store, documents):
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(
                chunk_size=Settings.chunk_size,
                chunk_overlap=Settings.chunk_overlap,
            ),
            Settings.embed_model,
        ],
        docstore=docstore,
        docstore_strategy="upserts",
        vector_store=vector_store,
    )

    # Run the ingestion pipeline and store the results
    nodes = pipeline.run(show_progress=True, documents=documents)

    return nodes

def persist_storage(docstore, vector_store):
    storage_context = StorageContext.from_defaults(
        docstore=docstore,
        vector_store=vector_store
    )
    storage_context.persist(STORAGE_DIR)

def generate_datasource(file: Optional[UploadFile] = None, web_urls: Optional[List[str]] = None):
    init_settings()
    logger.info("Generating index for the provided data")

    documents = load_documents(file, web_urls)
    docstore = get_doc_store()
    vector_store = get_vector_store()

    # Run the ingestion pipeline
    _ = run_pipeline(docstore, vector_store, documents)

    # Build the index and persist storage
    persist_storage(docstore, vector_store)

    logger.info("Finished generating the index")

