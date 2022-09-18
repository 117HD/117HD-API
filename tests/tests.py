import os
import sys
import pytest
import fastapi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import api.database.functions as functions


@pytest.mark.asyncio
async def test_rsn():
    assert await functions.is_valid_rsn("Ferrariic") == True
    with pytest.raises(fastapi.exceptions.HTTPException) as exc_info:
        assert await functions.is_valid_rsn("$$$$$$$$") == isinstance(
            exc_info.value, fastapi.exceptions.HTTPException
        )
