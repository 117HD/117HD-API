import json
import logging
import time
from typing import List, Optional

from api.config import redis_client
from api.database.functions import sha256
from fastapi import APIRouter, HTTPException, Request, status, Query
from pydantic import BaseModel

router = APIRouter()

logger = logging.getLogger(__name__)


class DiscordInformation(BaseModel):
    """sender's discord information"""

    discord_username: str
    discriminator: int
    discord_id: int


class SystemInformation(BaseModel):
    """sender's system information"""

    gpu: str
    cpu: str
    os: str
    opengl_version: str
    memory: int


class PluginInformation(BaseModel):
    """sender's plugin information"""

    settings: List[str]
    error: str


class submission(BaseModel):
    timestamp: Optional[int]  # will be overwritten
    discord: Optional[DiscordInformation]
    system: SystemInformation
    plugin: PluginInformation


@router.post("/v1/error-submission/post", tags=["LOGGING"])
async def post_error(submission: submission, request: Request) -> json:
    submission.timestamp = int(time.time())
    submission_dump = json.dumps(submission.json())

    key = sha256(f"{request.client.host}:{int(time.time())}")

    await redis_client.set(key, submission_dump)
    return {"key": key}


@router.get("/v1/error-submission/get", tags=["LOGGING"])
async def get_error(key: str, request: Request) -> json:
    data = await redis_client.get(key)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    data = json.loads(data)
    return json.loads(data)


@router.post("/v1/gpu/post", tags=["LOGGING"])
async def post_gpu(gpu: str, request: Request) -> json:
    await redis_client.incr(f"gpu:{gpu}", 1)
    return HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail=f"appended {gpu} to known unreliable GPUs",
    )


@router.get("/v1/gpu/get", tags=["LOGGING"])
async def get_gpu(request: Request, gpu=None) -> json:
    if gpu:
        data = await redis_client.get(f"gpu:{gpu}")
        data = int(data)
        return {"count": data}
    keys = await redis_client.keys("gpu:*")
    if not keys:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No known gpus listed. Start by appending a gpu using the /gpu/submit route!",
        )
    gpus = await redis_client.mget(keys=keys)
    if not gpus:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No known gpus listed. Start by appending a gpu using the /gpu/submit route!",
        )
    clean_keys = [key[len("gpu:") :] for key in keys]
    clean_counts = [int(g) for g in gpus]
    payload = dict(zip(clean_keys, clean_counts))
    return payload
