import aiofiles
import aiohttp
import hashlib
import jinja2
import urllib.parse
from typing import Any, Optional

from biisal.vars import Var
from biisal.bot import StreamBot
from biisal.utils.human_readable import humanbytes
from biisal.utils.file_properties import get_file_ids
from biisal.server.exceptions import InvalidHash

documentation = """
Async function to render a page for a file.

:param id: The ID of the file message.
:type id: int
:param secure_hash: The secure hash of the file.
:type secure_hash: str
:param src: The source URL of the file. Defaults to None.
:type src: Optional[str]
:return: The rendered page as a string.
:rtype: str
"""


async def render_page_async(id: int, secure_hash: str, src: Optional[str] = None) -> str:
    file_data = await get_file_ids(StreamBot, int(Var.BIN_CHANNEL), int(id))
    if not file_data:
        logging.debug(f"Invalid ID for message - ID {id}")
        raise InvalidHash

    if file_data.unique_id[:6] != hashlib.sha256(secure_hash.encode()).hexdigest()[:6]:
        logging.debug(f"link hash: {secure_hash} - {file_data.unique_id[:6]}")
        logging.debug(f"Invalid hash for message with - ID {id}")

