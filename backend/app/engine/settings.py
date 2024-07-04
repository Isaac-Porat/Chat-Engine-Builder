import os
import logging

from dotenv import load_dotenv

from llama_index.core.settings import Settings

load_dotenv()

logger = logging.getLogger("uvicorn")

def init_openai(model, temperature, embedding_model):
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    llm_config = {
        "model": model,
        "temperature": temperature,
        "api_key": api_key,
        # "max_tokens": None
    }

    llm = OpenAI(**llm_config)
    chunk_size = 1024
    chunk_overlap = 20


    embedding_config = {
        "model": embedding_model,
        "api_key": api_key,
        # "dimensions": None
    }
    embed_model = OpenAIEmbedding(**embedding_config)

    return llm, chunk_size, chunk_overlap, embed_model


def set_settings(model, llm_temperature, embedding_model):

    if model == "gpt-4":
        llm, chunk_size, chunk_overlap, embed_model = init_openai(model, llm_temperature, embedding_model)

        Settings.llm = llm
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        Settings.embed_model = embed_model

def init_settings():
    return {
        "llm": Settings.llm,
        "embed_model": Settings.embed_model,
        "chunk_size": Settings.chunk_size,
        "chunk_overlap": Settings.chunk_overlap
    }


# OpenAI Models
# gpt-4, gpt-4-32k, gpt-4-1106-preview, gpt-4-0125-preview, gpt-4-turbo-preview, gpt-4-vision-preview, gpt-4-1106-vision-preview, gpt-4-turbo-2024-04-09, gpt-4-turbo, gpt-4o, gpt-4o-2024-05-13, gpt-4-0613, gpt-4-32k-0613, gpt-4-0314, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-3.5-turbo-0125, gpt-3.5-turbo-1106, gpt-3.5-turbo-0613, gpt-3.5-turbo-16k-0613, gpt-3.5-turbo-0301, text-davinci-003, text-davinci-002, gpt-3.5-turbo-instruct, text-ada-001, text-babbage-001, text-curie-001, ada, babbage, curie, davinci, gpt-35-turbo-16k, gpt-35-turbo, gpt-35-turbo-0125, gpt-35-turbo-1106, gpt-35-turbo-0613, gpt-35-turbo-16k-0613