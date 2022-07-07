from sqlalchemy import true
import api.middleware
import api.database.functions as functions
from api.config import app, redis_client
import logging
import aioredis

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    await redis_client.incr(name="visits")
    visits = await redis_client.get(name="visits")
    return {"message": f"Welcome to the 117HD-API! Visited {int(visits)} times!"}
