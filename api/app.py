from sqlalchemy import true
import api.middleware
import api.database.functions as functions
from api.config import app, redis_client
import logging
import aioredis
from api.routers import submission

logger = logging.getLogger(__name__)

app.include_router(submission.router)


@app.on_event("startup")
async def startup():
    # declare api start
    logger.info(f"STARTED 117HD-API")

    # check redis server
    if await redis_client.ping():
        logger.info("REDIS SERVER CONNECTED!")
    else:
        logger.fatal("REDIS SERVER IS NOT ACCESSIBLE!")


@app.on_event("shutdown")
async def shutdown():
    # declare api shutdown
    logger.info(f"SHUTDOWN 117HD-API")


@app.get("/")
async def root():
    return {"message": f"Welcome to the 117HD-API!"}
