import logging
from llama_index.core.indices import VectorStoreIndex
from engine.index.vectordb import get_vector_store

logger = logging.getLogger("uvicorn")

def get_index():
    logger.info("Connecting to vector store...")

    store = get_vector_store()

    index = VectorStoreIndex.from_vector_store(store)

    logger.info("Finished loading index from vector store...")

    return index