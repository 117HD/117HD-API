import logging
import re

from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def is_valid_rsn(login: str) -> bool:
    if not re.fullmatch("[\w\d\s_-]{1,12}", login):
        raise HTTPException(
            status_code=202,
            detail=f"bad rsn",
        )
    return True
