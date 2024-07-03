import os
import logging
import tempfile
from fastapi import UploadFile, HTTPException

logger = logging.getLogger("uvicorn")

def get_file_documents(file: UploadFile):
    from llama_index.core.readers import SimpleDirectoryReader

    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = file.read()
            temp_file.write(content)
            temp_file.flush()

        reader = SimpleDirectoryReader(input_files=[temp_file.name])
        return reader.load_data()

    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e.detail)
        )

    except Exception as e:
        logger.error(f"Error loading file documents {str(e)}")


