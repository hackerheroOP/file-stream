import jinja2
import re
import time
import math
import logging
import secrets
import mimetypes
from aiohttp import web, ContentTypeError
from aiohttp.http_exceptions import BadStatusLine, ConnectionResetError
from typing import Any, Dict, List, Optional, Tuple

import biisal.bot
import biisal.server.exceptions
from biisal.utils.time_format import get_readable_time
from biisal.utils.custom_dl import ByteStreamer
from biisal.utils.render_template import render_page
from biisal.vars import Var

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = web.Application()
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request: web.Request) -> web.Response:
    """
    Handles the root route and returns the server status page.
    """
    google_tag_code = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0K633G9XYB"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-0K633G9XYB');
    </script>
    """

    html_content = """
    <html>
        <head>
            {google_tag_code}
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f0f0f0;
                }}
                h1 {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #333;
                    padding: 20px;
                    background-color: #ddd;
                    border-bottom: 1px solid #ccc;
                }}
                p {{
                    font-size: 1.1em;
                    color: #333;
                    padding: 20px;
                }}
                ul {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }}
                li {{
                    padding: 5px 0;
                    border-bottom: 1px solid #ccc;
                }}
            </style>
        </head>
        <body>
            <h1>Link Wiz Status</h1>
            <p>Server status: <strong>{server_status}</strong></p>
            <p>Uptime: <strong>{uptime}</strong></p>
            <p>Telegram bot: <strong>{telegram_bot}</strong></p>
            <p>Connected bots: <strong>{connected_bots}</strong></p>
            <p>Loads:</p>
            <ul>
                {loads}
            </ul>
            <p>Version: <strong>{version}</strong></p>
        </body>
    </html>
    """.format(
        google_tag_code=google_tag_code,
        server_status="running",
        uptime=get_readable_time(time.time() - biisal.bot.StartTime),
        telegram_bot="@" + biisal.bot.StreamBot.username,
        connected_bots=len(biisal.bot.multi_clients),
        loads="".join(
            f"<li>Bot {c + 1}: {l}</li>"
            for c, (_, l) in enumerate(
                sorted(biisal.bot.work_loads.items(), key=lambda x: x[1], reverse=True)
            )
        ),
        version=biisal.__version__,
    )
    return web.Response(body=html_content, content_type="text/html")

@routes.get("/watch/{path:.*}", allow_head=True)
async def stream_handler(request: web.Request) -> web.Response:
    """
    Handles the /watch route and returns the media stream.
    """
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(text=await render_page(id, secure_hash), content_type="text/html")
    except biisal.server.exceptions.InvalidHash as e:
        raise web.HTTPForbidden(text=e.message) from e
    except biisal.server.exceptions.FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message) from e
    except (
        AttributeError,
        BadStatusLine,
        ConnectionResetError,
        ContentTypeError,
    ) as e:
        logger.error(e)
        pass
    except Exception as e:
        logger.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

@routes.get("/{path:.*}", allow_head=True)
async def stream_handler(request: web.Request) -> web.Response:
    """
    Hand
