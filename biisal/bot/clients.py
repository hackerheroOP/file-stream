import asyncio
import logging
from typing import Dict, Any, List, Tuple, Coroutine
from ..vars import Var
from pyrogram import Client
from pyrogram.errors import StartRequested
from biisal.utils.config_parser import TokenParser
from . import multi_clients, work_loads, StreamBot
import aiosignal

async def initialize_clients() -> None:
    """
    Initialize and start Pyrogram clients.
    """
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    all_tokens = TokenParser().parse_from_env()
    if not all_tokens:
        print("No additional clients found, using default client")
        return

    async def start_client(client_id: int, token: str) -> Coroutine[Any, Any, Tuple[int, Client]]:
        """
        Start a Pyrogram client with the given ID and token.
        """
        try:
            print(f"Starting - Client {client_id}")
            if client_id == len(all_tokens):
                print("This will take some time, please wait...")
                await asyncio.sleep(2)
            async with Client(
                name=str(client_id),
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=token,
                sleep_threshold=Var.SLEEP_THRESHOLD,
                no_updates=True,
                in_memory=True,
            ) as client:
                await client.start()
                work_loads[client_id] = 0
                return client_id, client
        except Exception:
            logging.error(f"Failed starting Client - {client_id}", exc_info=True)

    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True
        print("Multi-Client Mode Enabled")
    else:
        print("No additional
