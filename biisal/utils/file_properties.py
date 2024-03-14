from pyrogram import Client    # Importing Client class from pyrogram library
from typing import Any, Optional    # Importing Any and Optional types from typing library
from pyrogram.types import Message    # Importing Message class from pyrogram.types library
from pyrogram.file_id import FileId    # Importing FileId class from pyrogram.file_id library
from pyrogram.raw.types.messages import Messages    # Importing Messages class from pyrogram.raw.types.messages library
from biisal.server.exceptions import FIleNotFound    # Importing FileNotFound exception from biisal.server.exceptions library

async def parse_file_id(message: "Message") -> Optional[FileId]:
    """
    Decodes the file_id from the given message object and returns it as a FileId object.
    If the message object does not contain any media, it returns None.
    """
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

async def parse_file_unique_id(message: "Messages") -> Optional[str]:
    """
    Returns the file_unique_id from the given message object as a string.
    If the message object does not contain any media, it returns None.
    """
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id

async def get_file_ids(client: Client, chat_id: int, id: int) -> Optional[FileId]:
    """
    Retrieves the message object with the given chat_id and id from the server using the client object.
    If the message object is empty or does not contain any media, it raises a FileNotFound exception.
    Otherwise, it extracts the required attributes from the media object and sets them to the FileId object.
    Finally, it returns the FileId object.
    """
    message = await client.get_messages(chat_id, id)
    if message.empty:
        raise FIleNotFound
    media = get_media_from_message(message)
    file_unique_id = await parse_file_unique_id(message)
    file_id = await parse_file_id(message)
    setattr(file_id, "file_size", getattr(media, "file_size", 0))
    setattr(file_id, "mime_type", getattr(media, "mime_type", ""))
    setattr(file_id, "file_name", getattr(media, "file_name", ""))
    setattr(file_id, "unique_id", file_unique_id)
    return file_id

def get_media_from_message(message: "Message") -> Any:
    """
    Returns the first media object found in the given message object.
    It checks for the following media types in order: audio, document, photo, sticker, animation, video, voice, and video_note.
    If no media object is found, it returns None.
    """
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
       
