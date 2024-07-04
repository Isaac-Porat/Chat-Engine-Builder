import os
from engine.index.index import get_index
from fastapi import HTTPException

def get_chat_engine():
    system_prompt = "Hello..."
    top_k = 3

    index = get_index()
    if index is None:
        raise HTTPException(
            status_code=500,
            detail=str(
                "Error getting index..."
            ),
        )

    return index.as_chat_engine(
        similarity_top_k=int(top_k),
        system_prompt=system_prompt,
        chat_mode="condense_plus_context",
    )