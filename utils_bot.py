import logging # Importing the logging module for logging purposes
import os # Importing the os module for operating system dependent functionality
import threading # Importing the threading module for working with threads
import time # Importing the time module for working with time
from asyncio import TimeoutError # Importing TimeoutError from asyncio module
from pyrogram import filters # Importing filters from pyrogram module

# Creating a logger instance
# The 'getLogger' function is used to get a logger instance, which is used to log messages.
# The name of the logger is set to '__name__', which is the name of the current module.
LOGGER = logging.getLogger(__name__)

# Define a list of units for file size
# This is a list of string values that represent different units of file size.
# It includes bytes, kilobytes, megabytes, gigabytes, terabytes, and petabytes.
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

# Define a class for setting an interval for a function to execute
class setInterval:
    def __init__(self, interval, action):
        """
        Initialize the setInterval class with an interval and an action to be executed.
        The '__init__' method is a special method that is called when an instance of the class is created.
        It takes two arguments: 'interval' and 'action'.
        The 'interval' argument is the time in seconds between each execution of the 'action' function.
        The 'action' argument is the function that will be executed at the specified interval.
        """
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event() # Create a threading event to stop the interval
        thread = threading.Thread(target=self.__setInterval) # Create a new thread for the interval
        thread.start() # Start the thread

    def __setInterval(self):
        """
        The method that sets the interval for the action to be executed.
        This method is called in a separate thread, and it is responsible for executing the 'action' function
        at the specified interval.
        """
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        """
        Method to cancel the interval.
        This method is used to stop the interval and prevent the 'action' function from being executed any further.
        """
        self.stopEvent.set()

# Function to get the readable file size
def get_readable_file_size(size_in_bytes) -> str:
    """
    Function to convert the file size in bytes to a human readable format.
    This function takes a single argument 'size_in_bytes', which is the file size in bytes.
    It returns a string representation of the file size in a human readable format.
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
    This function takes a single argument 'seconds', which is the time in seconds.
    It returns a string representation of the time in a human readable format.
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
    This function is identical to the
