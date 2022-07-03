from datetime import datetime
from email.policy import default
from typing import Text
from numpy import integer
from sqlalchemy import (
    INTEGER,
    TIMESTAMP,
    VARCHAR,
    BigInteger,
    Column,
    ForeignKey,
    Boolean,
    Integer,
)
from sqlalchemy.dialects.mysql import TEXT, TINYINT, VARCHAR
from sqlalchemy.dialects.mysql.types import TINYTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# generated with sqlacodegen
Base = declarative_base()
metadata = Base.metadata


### BOILERPLATE
