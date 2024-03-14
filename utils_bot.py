import logging # Importing the logging module for logging purposes
import os # Importing the os module for operating system dependent functionality
import threading # Importing the threading module for working with threads
import time # Importing the time module for working with time
from asyncio import TimeoutError # Importing TimeoutError from asyncio module
from pyrogram import filters # Importing filters from pyrogram module

# Creating a logger instance
LOGGER = logging.getLogger(__name__)

# Define a list of units for file size
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

# Define a class for setting an interval for a function to execute
class setInterval:
    def __init__(self, interval, action):
        """
        Initialize the setInterval class with an interval and an action to be executed.
        """
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event() # Create a threading event to stop the interval
        thread = threading.Thread(target=self.__setInterval) # Create a new thread for the interval
        thread.start() # Start the thread

    def __setInterval(self):
        """
        The method that sets the interval for the action to be executed.
        """
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        """
        Method to cancel the interval.
        """
        self.stopEvent.set()

# Function to get the readable file size
def get_readable_file_size(size_in_bytes) -> str:
    """
    Function to convert the file size in bytes to a human readable format.
    """
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

# Function to get the readable time
def get_readable_time(seconds: int) -> str:
    """
    Function to convert the time in seconds to a human readable format.
    """
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

# Function to get the readable time
def readable_time(seconds: int) -> str:
    """
    Function to convert the time in seconds to a human readable format.
    """
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
