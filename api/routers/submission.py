import json
import logging
import time
from typing import List, Optional

from api.config import redis_client
from api.database.functions import sha256
from fastapi import APIRouter, HTTPException, Request
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


@router.post("/v1/error-submission/submit", tags=["LOGGING"])
async def submit(submission: submission, request: Request) -> json:
    submission.timestamp = int(time.time())
    submission_dump = json.dumps(submission.json())

    key = sha256(f"{request.client.host}:{int(time.time())}")

    await redis_client.set(key, submission_dump)
    return {"key": key}


@router.get("/v1/error-submission/retrieve", tags=["LOGGING"])
async def retrieve(key: str, request: Request) -> json:
    data = await redis_client.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="Not found")
    data = json.loads(data)
    return json.loads(data)
