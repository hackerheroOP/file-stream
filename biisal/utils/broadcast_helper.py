# (c) @biisal, adarsh-goel

import asyncio # Importing asyncio library for asynchronous programming
import traceback # Importing traceback library for printing detailed error tracebacks
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid # Importing specific exceptions from pyrogram library

MAX_RETRIES = 5 # Defining maximum number of retries before giving up

async def send_msg(user_id, message):
    """
    Asynchronous function to send a message to a user.

    Args:
        user_id (int): The ID of the user to send the message to.
        message (Message): The message object to be sent.

    Returns:
        tuple: A tuple containing a status code and an error message (if any).
            200 indicates success, while any other value indicates an error.
    """
    if not user_id or not message:
        # Returning an error if user_id or message is not provided
        return 400, "Invalid arguments"

    retries = 0 # Initializing retries to 0

    while True:
        try:
            # Trying to forward the message to the specified user_id
            await message.forward(chat_id=user_id)
            return 200, None # Returning 200 if successful
        except FloodWait as e:
            # If FloodWait exception is raised, waiting for the specified time before retrying
            if retries >= MAX_RETRIES:
                return 500, f"{user_id} : FloodWait exceeded the maximum number of retries\n" # Returning an error if the maximum number of retries is reached
            
            await asyncio.sleep(e.x) # Waiting for the specified time
            retries += 1 # Incrementing retries
        except InputUserDeactivated:
            # Returning an error if the user is deactivated
            return 400, f"{user_id} : deactivated\n"
        except User
