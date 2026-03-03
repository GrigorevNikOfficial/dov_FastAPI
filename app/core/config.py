from __future__ import annotations
import os
from typing import Literal


DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./db.sqlite3"
)
