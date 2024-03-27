import logging
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Form
)
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys

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
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        output = result.stdout
        error = result.stderr

        return {"output": output, "error": error}

    except Exception as e:
        log.exception(e)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )