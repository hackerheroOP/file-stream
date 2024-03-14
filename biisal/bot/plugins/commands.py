import logging
import asyncio
from typing import Union  # for specifying union types in type hints

import pyrogram  # a Python wrapper for the Telegram API
from pyrogram.errors import UserNotParticipant, FloodWait  # specific Pyrogram exceptions

# Initialize a logger for this module
logger = logging.getLogger(__name__)

async def some_function(...):
    """
    This is a brief description of what this function does.

    :param arg1: Description of the first argument
    :param arg2: Description of the second argument
    :return: Description of the return value(s)
    """
    # Do something asynchronously
    await some_coroutine()

    # Handle UserNotParticipant exception
    try:
        # Do something that might raise a UserNotParticipant exception
        await pyrogram_client.send_message(...)
    except UserNotParticipant:
        logger.warning("User is not a participant in the chat")

    # Handle FloodWait exception
    try:
        # Do something that might raise a FloodWait exception
        await pyrogram_client.send_message(...)
    except FloodWait as e:
        logger.warning(f"FloodWait exception: {e.x} seconds")

# Initialize a Pyrogram client
pyrogram_client = pyrogram.Client(...)

# Define a main function to run the script
async def main():
    # Do something with the Pyrogram client
    await pyrogram_client.start()

# Run the main function asynchronously
asyncio.run(main())
