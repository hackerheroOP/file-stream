# (c) @biisal, Adarsh-Goel
import datetime
import motor.motor_asyncio
from typing import Optional

class Database:
    """
    A class representing a database connection and its components.
    
    This class initializes a MongoDB connection using the `motor.motor_asyncio` library,
    and sets references to the specified database and collections ('users' and 'banned\_list').
    """

    def __init__(self, uri: str, database_name: str):
        """
        Initialize the Database object with a URI and database name.

        :param uri: The URI for the database connection
        :param database_name: The name of the database
        """
        # Initialize the MongoDB client with the provided URI
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        
        # Select the specified database
        self.db = self._client[database_name]
        
        # Set a reference to the 'users' collection
        self.col = self.db.users
        
        # Set a reference to the 'banned_list' collection
        self.banned_list = self.db.banned_list
