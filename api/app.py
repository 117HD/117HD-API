from sqlalchemy import true
import api.middleware
import api.database.functions as functions
from api.config import app
import logging

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Welcome to the 117HD-API!"}
