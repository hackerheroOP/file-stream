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
        """A custom class that holds the cache of a specific client and class functions.
        attributes:
            client: the client that the cache is for.
            cached_file_ids: a dict of cached file IDs.
            cached_file_properties: a dict of cached file properties.

        functions:
            generate_file_properties: returns the properties for a media of a specific message contained in Tuple.
            generate_media_session: returns the media session for the DC that contains the media file.
            yield_file: yield a file from telegram servers for streaming.
        """
        self.clean_timer = 30 * 60
        self.client = client
        self.cached_file_ids: Dict[int, FileId] = {}
        asyncio.create_task(self.clean_cache())

    def __str__(self):
        return f"ByteStreamer(client={self.client})"

    async def get_file_properties(self, id: int) -> FileId:
        """
        Returns the properties of a media of a specific message in a FIleId class.
        if the properties are cached, then it'll return the cached results.
        or it'll generate the properties from the Message ID and cache them.
        """
        if id not in self.cached_file_ids:
            await self.generate_file_properties(id)
            logging.debug(f"Cached file properties for message with ID {id}")
        return self.cached_file_ids[id]

    async def generate_file_properties(self, id: int) -> FileId:
        """
        Generates the properties of a media file on a specific message.
        returns ths properties in a FIleId class.
        """
        file_id = await get_file_ids(self.client, id)
        logging.debug(f"Generated file ID and Unique ID for message with ID {id}")
        if not file_id:
            logging.debug(f"Message with ID {id} not found")
            raise FIleNotFound
        self.cached_file_ids[id] = file_id
        logging.debug(f"Cached media message with ID {id}")
        return self.cached_file_ids[id]

    async def generate_media_session(self, client: pyrogram.Client, file_id: FileId) -> Session:
        """
        Generates the media session for the DC that contains the media file.
        This is required for getting the bytes from Telegram servers.
        """
        media_session = client.media_sessions.get(file_id.dc_id, None)

        if media_session is None:
            if file_id.dc_id != await client.storage.dc_id():
                media_session = Session(
                    client,
                    file_id.dc_id,
                    await Auth(client, file_id.dc_id, await client.storage.test_mode()).create(),
                    await client.storage.test_mode(),
                    is_media=True,
                ).create()
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
                ).create()
                await media_session.start()
            logging.debug(f"Created media session for DC {file_id.dc_id}")
            client.media_sessions[file_id.dc_id] = media_session
        else:
            logging.debug(f"Using cached media session for DC {file_id.dc_id}")
        return media_session

    @staticmethod
    async def get_location(file_id: FileId) -> Union[InputPhotoFileLocation, InputDocumentFileLocation, InputPeerPhotoFileLocation]:
        """
        Returns the file location for the media file.
        """
        file_type = file_id.file_type

        if file_type == FileType.CHAT_PHOTO:
            if file_id.chat_id > 0:
                peer = InputPeerUser(
                    user_id=file_id.chat_id, access_hash=file_id.chat_access_hash
                )
            else:
                if file_id.chat_access_hash == 0:
                    peer = InputPeerChat(chat_id
