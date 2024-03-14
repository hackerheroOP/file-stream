import asyncio
import logging
import aiohttp
import traceback
from biisal.vars import Var

async def ping_server():
    """
    This function pings the server at the specified URL after a certain sleep time.
    It handles TimeoutError and other exceptions, logging relevant information.
    """
    sleep_time = Var.PING_INTERVAL  # Set the sleep time based on the PING_INTERVAL variable
    while True:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                """
                Create an asynchronous context manager for an aiohttp ClientSession.
                Set the total timeout to 10 seconds.
                """
                async with session.get(Var.URL) as response:
                    """
                    Send a GET request to the server URL using the aiohttp ClientSession.
                    Store the response object in the 'response' variable.
                    """
                    logging.info(f"Pinged server with response: {response.status}")
                    """
                    Log the response status code using the logging.info() method.
                    """
        except asyncio.TimeoutError:
            logging.warning("Couldn't connect to the server URL within the timeout limit..!")
            """
            Log a warning message if the connection to the server times out.
            """
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            """
            Log an error message with the exception details if any other exception occurs.
            """
            traceback.print_exc()
            """
            Print the traceback for debugging purposes.
            """
        finally:
            await asyncio.sleep(sleep_time)
            """
            Sleep for the specified sleep time before the next iteration.
            """
