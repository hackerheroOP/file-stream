from pyrogram import Client    # Importing Client class from pyrogram library
from typing import Any, Optional    # Importing Any and Optional types from typing library
from pyrogram.types import Message    # Importing Message class from pyrogram.types library
from pyrogram.file_id import FileId    # Importing FileId class from pyrogram.file_id library
from pyrogram.raw.types.messages import Messages    # Importing Messages class from pyrogram.raw.types.messages library
from biisal.server.exceptions import FIleNotFound    # Importing FileNotFound exception from biisal.server.exceptions library

async def parse_file_id(message: "Message") -> Optional[FileId]:
    """
    This function decodes the file_id from the given message object and returns it as a FileId object.
    If the message object does not contain any media, it returns None.
    """
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

