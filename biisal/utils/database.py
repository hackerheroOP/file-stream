# (c) @biisal, Adarsh-Goel
import datetime
import motor.motor_asyncio
from typing import Optional

class Database:
    """
    A class representing a database connection and its components.
    """

    def __init__(self, uri: str, database_name: str):
        """
        Initialize the Database object with a URI and database name.

        :param uri: The URI for the database connection
        :param database_name: The name of the database
        """
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)  # Initialize the MongoDB client
        self.db = self._client[database_name]  # Select the specified database
        self.col = self.db.users  # Set a reference to the 'users' collection
        self.banned_list = self.db.banned_list  # Set a reference to the 'banned_list' collection
