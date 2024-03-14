import asyncio
import logging
from typing import Dict, Any, List, Tuple, Coroutine
from ..vars import Var
from pyrogram import Client
from pyrogram.errors import StartRequested
from biisal.utils.config_parser import TokenParser
from . import multi_clients, work_loads, StreamBot  # Importing required modules and global variables

async def initialize_clients() -> None:
    """
    Initialize and start Pyrogram clients.
    This function initializes and starts Pyrogram clients using the tokens provided in the environment variables.
    If no additional clients are found, it uses the default client.
    """
    multi_clients[0] = StreamBot  # Assign the first client as StreamBot
    work_loads[0] = 0  # Initialize workload for the first client as 0

    all_tokens = TokenParser().parse_from_env()  # Parse tokens from environment variables
    if not all_tokens:
        print("No additional clients found, using default client")
        return

    async def start_client(client_id: int, token: str) -> Coroutine[Any, Any, Tuple[int, Client]]:
        """
        Start a Pyrogram client with the given ID and token.
        This is a helper function that starts a Pyrogram client asynchronously with the given client_id and token.
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
                await client.start()  # Start the client
                work_loads[client_id] = 0  # Initialize workload for the client as 0
                return client_id, client  # Return the client_id and client instance
        except Exception:
            logging.error(f"Failed starting Client - {client_id}", exc_info=True)

    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])  # Start all clients asynchronously
    multi_clients.update(dict(clients))  # Update the multi_clients dictionary with the new client instances
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True  # Set the MULTI_CLIENT variable to True if there is more than one client
        print("Multi-Client Mode Enabled")
    else:
        print("No additional clients found")
