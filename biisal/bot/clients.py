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
    # Assign the first client as StreamBot
    multi_clients[0] = StreamBot
    
    # Initialize workload for the first client as 0
    work_loads[0] = 0

    # Parse tokens from environment variables
    all_tokens = TokenParser().parse_from_env()
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

            # If the client_id is the same as the length of all_tokens, it means this is the last client,
            # and it might take some time to start, so notify the user
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

                # Initialize workload for the client as 0
                work_loads[client_id] = 0

                return client_id, client  # Return the client_id and client instance
        except Exception:
            logging.error(f"Failed starting Client - {client_id}", exc_info=True)

    # Start all clients asynchronously
    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])

    # Update the multi_clients dictionary with the new client instances
    multi_clients.update(dict(clients))

    # If there is more than one client, enable Multi-Client Mode
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True  # Set the MULTI_CLIENT variable to True
        print("Multi-Client Mode Enabled")
    else:
        print("No additional clients found")
