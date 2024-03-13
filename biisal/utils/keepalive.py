import asyncio
import logging
import aiohttp
import traceback
from biisal.vars import Var

async def ping_server():
    sleep_time = Var.PING_INTERVAL
    while True:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(Var.URL) as response:
                    logging.info(f"Pinged server with response: {response.status}")
        except asyncio.TimeoutError:
            logging.warning("Couldn't connect to the server URL within the timeout limit..!")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
        finally:
            await asyncio.sleep(sleep_time)
