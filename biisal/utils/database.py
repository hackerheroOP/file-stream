# (c) @biisal, Adarsh-Goel
import datetime
import motor.motor_asyncio
from typing import Optional

class Database:
    def __init__(self, uri: str, database_name: str):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.banned_list = self.db.banned_list

