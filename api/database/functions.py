import logging
import re
import hashlib

from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def is_valid_rsn(login: str) -> bool:
    if not re.fullmatch("[\w\d\s_-]{1,12}", login):
        raise HTTPException(
            status_code=202,
            detail=f"bad rsn",
        )
    return True


def sha256(string: str) -> str:
    """sha256 encodes a string"""
    return hashlib.sha256(string.encode()).hexdigest()
