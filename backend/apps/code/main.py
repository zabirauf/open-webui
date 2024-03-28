import logging
import requests
import json
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Form
)
from fastapi.middleware.cors import CORSMiddleware

from constants import ERROR_MESSAGES
from utils.utils import (
    get_current_user,
)
from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["CODE"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/run")
def run_code(
    code: str = Form(...),
    language: str = Form(...),
    user=Depends(get_current_user),
):
    log.info(f"code: {code}")

    if not code or code == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(),
        )

    if language != "python":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language not supported",
        )
    try:
        # Execute code
        output, error = execute_code(code, language)

        return {"output": output, "error": error}

    except Exception as e:
        log.exception(e)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


def execute_code(code, language='python'):
    try:
        language_version = try_init_language_runtime()

        url = "http://localhost:3001/api/v2/execute"
        headers = {"Content-Type": "application/json"}
        payload = {
            "language": language,
            "version": language_version,
            "files": [
                {
                    "name": "code.py",
                    "content": code
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        output = data['run']['stdout']
        error = data['run']['stderr']
        return output, error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, str(e)


def try_init_language_runtime():
    # TODO: This should take in language and return correct version
    try:
        url = "http://localhost:3001/api/v2/runtimes"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        languages = [runtime['language'] for runtime in data]
        if 'python' not in languages:
            headers = {"Content-Type": "application/json"}
            payload = {
                "language": "python",
                "version": "3.9.4"
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        return "3.9.4"
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, str(e)
