import json
import logging
import os
import sys
import warnings
import aioredis

# import logging_loki
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# load environment variables
load_dotenv(find_dotenv(), verbose=True)


class Configuration:
    def __init__(self):
        self.sql_uri = os.environ.get("sql_uri")
        self.REDIS_PASSWORD = os.environ.get("redis_password")
        self.REDIS_DATABASE = os.environ.get("redis_database")
        self.REDIS_PORT = int(os.environ.get("redis_port"))
        self.API_VERSION = os.environ.get("api_version")


configVars = Configuration()

redis_client = aioredis.from_url(
    url="redis://51.89.216.169",
    port=configVars.REDIS_PORT,
    db=configVars.REDIS_DATABASE,
    password=configVars.REDIS_PASSWORD,
)

# create application
app = FastAPI(
    title="117HD-API",
    version=f"{configVars.API_VERSION}",
    contact={
        "name": "117HD-API",
        "url": "https://discord.gg/U4p6ChjgSE",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

file_handler = logging.FileHandler(filename="logs/error.log", mode="a")
stream_handler = logging.StreamHandler(sys.stdout)

# log formatting
formatter = logging.Formatter(
    json.dumps(
        {
            "ts": "%(asctime)s",
            "name": "%(name)s",
            "function": "%(funcName)s",
            "level": "%(levelname)s",
            "msg": json.dumps("%(message)s"),
        }
    )
)


file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

handlers = [file_handler, stream_handler]

logging.basicConfig(level=logging.DEBUG, handlers=handlers)

# set imported loggers to warning
logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("uvicorn").setLevel(logging.DEBUG)

logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("aiomysql").setLevel(logging.ERROR)

logging.getLogger("uvicorn.error").propagate = False


# https://github.com/aio-libs/aiomysql/issues/103
# https://github.com/coleifer/peewee/issues/2229
warnings.filterwarnings("ignore", ".*Duplicate entry.*")
