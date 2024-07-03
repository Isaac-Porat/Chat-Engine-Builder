from llama_index.core.settings import Settings
from models import ChatEngineSettings

def init_openai(model, temperature, embedding_model):
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI

    llm_config = {
        "model": model,
        "temperature": temperature,
        # "max_tokens": None
    }
    Settings.llm = OpenAI(**llm_config)


    embedding_config = {
        "model": embedding_model,
        # "dimensions": None
    }
    Settings.embed_model = OpenAIEmbedding(**embedding_config)


def init_settings(model, llm_temperature, embedding_model):
    model = model
    llm_temp = llm_temperature
    embedding_model = embedding_model

    if model == "gpt-4":
        init_openai(model, llm_temp, embedding_model)

