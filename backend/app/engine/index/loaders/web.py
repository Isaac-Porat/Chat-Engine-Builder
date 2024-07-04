import logging
from pydantic import BaseModel, Field
from typing import List

logger = logging.getLogger("uvicorn")

class CrawlUrl(BaseModel):
    base_url: str
    prefix: str = ""
    # max_depth: int = Field(default=1, ge=0)
    max_depth: int = 0 # for testing purposes only

def get_web_documents(urls: List[str]):
    config = [CrawlUrl(base_url=url) for url in urls]

    from llama_index.readers.web import WholeSiteReader
    from selenium import webdriver

    docs = []
    for url in config:
        scraper = WholeSiteReader(
            prefix=url.prefix,
            max_depth=url.max_depth,
            driver=webdriver.Chrome()
        )
        docs.extend(scraper.load_data(url.base_url))

    return docs