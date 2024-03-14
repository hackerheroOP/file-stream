import asyncio
import logging
import math
from typing import Dict, Union

import pyrogram
from pyrogram.errors import AuthBytesInvalid, FileNotFound
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from pyrogram.raw.functions.auth import ExportAuthorization, ImportAuthorization
from pyrogram.raw.functions.upload import GetFile
from pyrogram.session import Session, Auth
from pyrogram.types import InputPeerUser, InputPeerChat, InputPeerChannel, InputPhotoFileLocation, InputDocumentFileLocation, InputPeerPhotoFileLocation

class ByteStreamer:
    def __init__(self, client: pyrogram.Client):
        """
        Initialize a ByteStreamer object with a pyrogram.Client instance.

        :param client: The pyrogram.Client instance to use for caching file IDs and properties.
        """
        self.clean_timer = 30 * 60  # Clean cache every 30 minutes.
        self.client = client
        self.cached_file_ids: Dict[int, FileId] = {}  # Cache for file IDs.
        asyncio.create_task(self.clean_cache())  # Start cleaning the cache in the background.

    def __str__(self):
        """
        Return a string representation of the ByteStreamer object.

        :return: A string representation of the ByteStreamer object.
        """
        return f"ByteStreamer(client={self.client})"

    async def get_file_properties(self, id: int) -> FileId:
        """
        Get the properties of a media file from the cache or generate them if they don't exist.

        :param id: The ID of the message containing the media file.
        :return: The FileId instance containing the properties of the media file.
        """
        if id not in self.cached_file_ids:
            await self.generate_file_properties(id)
            logging.debug(f"Cached file properties for message with ID {id}")
        return self.cached_file_ids[id]

    async def generate_file_properties(self, id: int) -> FileId:
        """
        Generate the properties of a media file and cache them.

        :param id: The ID of the message containing the media file.
        :return: The FileId instance containing the properties of the media file.
        """
        file_id = await get_file_ids(self.client, id)  # Generate the file ID.
        logging.debug(f"Generated file ID and Unique ID for message with ID {id}")
        if not file_id:
            logging.debug(f"Message with ID {id} not found")
            raise FIleNotFound  # Raise a custom exception if the message is not found.
        self.cached_file_ids[id] = file_id  # Cache the file ID.
        logging.debug(f"Cached media message with ID {id}")
        return self.cached_file_ids[id]

    async def generate_media_session(self, client: pyrogram.Client, file_id: FileId) -> Session:
        """
        Generate a media session for the DC that contains the media file.

        :param client: The pyrogram.Client instance to use for creating the media session.
        :param file_id: The FileId instance containing the properties of the media file.
        :return: The Session instance for the media session.
        """
        media_session = client.media_sessions.get(file_id.dc_id, None)  # Get the media session from the cache.

        if media_session is None:
            if file_id.dc_id != await client.storage.dc_id():  # If the DC is different from the current DC.
                media_session = Session(
                    client,
                    file_id.dc_id,
                    await Auth(client, file_id.dc_id, await client.storage.test_mode()).create(),
                    await client.storage.test_mode(),
                    is_media=True,
                ).create()  # Create a new media session.
                await media_session.start()

                for _ in range(6):
                    exported_auth = await client.invoke(
                        ExportAuthorization(dc_id=file_id.dc_id)
                    )

                    try:
                        await media_session.send(
                            ImportAuthorization(
                                id=exported_auth.id, bytes=exported_auth.bytes
                            )
                        )
                        break
                    except AuthBytesInvalid:
                        logging.debug(
                            f"Invalid authorization bytes for DC {file_id.dc_id}"
                        )
                        continue
                else:
                    await media_session.stop()
                    raise AuthBytesInvalid
            else:
                media_session = Session(
                    client,
                    file_id.dc_id,
                    await client.storage.auth_key(),
                    await client.storage.test_mode(),
                    is_media=True,
                ).create()  # Create a new media session.
                await media_session.start()
            logging.debug(f"Created media session for DC {file_id.dc_id}")
            client.media_sessions[file_id.dc_id] = media_session  # Cache the media session.
        else:
            logging.debug(f"Using cached media session for DC {file_id.dc_id}")
        return media_session

    @staticmethod
    async def get_location(file_id: FileId) -> Union[InputPhotoFileLocation, InputDocumentFileLocation, InputPeerPhotoFileLocation]:
        """
        Get the file location for the media file.

        :param file_id: The FileId instance containing the properties of the media file.
        :return: The file location as a InputPhotoFileLocation, InputDocumentFileLocation, or InputPeerPhotoFileLocation instance.
        """
        file_type = file_id.file_type

        if file_type == FileType.CHAT_PHOTO:
            if file_id.chat_id > 0:
               
