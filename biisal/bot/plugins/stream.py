# Importing required modules
# pylint: disable=import-error,no-name-in-module
import os
import asyncio
from asyncio import TimeoutError
from biisal.bot import StreamBot
from biisal.utils.database import Database
from biisal.utils.human_readable import humanbytes
from biisal.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Local imports
# from utils_bot import get_shortlink

# Importing file properties utility functions
from biisal.utils.file_properties import get_name, get_hash, get_media_file_size

# Initializing the database connection
# The 'Var.DATABASE_URL' and 'Var.name' are imported from 'biisal.vars' module
db = Database(Var.DATABASE_URL, Var.name)

# Defining a dictionary for storing passwords and initializing a password database
MY_PASS = os.environ.get("MY_PASS", None)
# The 'os.environ.get("MY_PASS", None)' is used to get the environment variable 'MY_PASS'
# If it is not set, 'None' is assigned to 'MY_PASS'
pass_dict = {}
# Initializing an empty dictionary for storing passwords
pass_db = Database(Var.DATABASE_URL, "ag_passwords")
# Initializing the password database connection

# Defining a message text template
msg_text = """<b>‣ ʏᴏᴜʀ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ! 😎

‣ Fɪʟᴇ ɴᴀᴍᴇ : <i>{}</i>
‣ Fɪʟᴇ ꜱɪᴢᴇ : {}

🔻 <a href="{}">𝗙𝗔𝗦𝗧 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗</a>
🔺 <a href="{}">𝗪𝗔𝗧𝗖𝗛 𝗢𝗡𝗟𝗜𝗡𝗘</a>

‣ ɢᴇᴛ <a href="https://t.me/movies_desire_bot">ᴍᴏʀᴇ ғɪʟᴇs</a></b> 🤡""\"
"""
# The 'msg_text' is a message template for sending a message to the user
# It contains placeholders for file name, file size, and file links

# Defining the event handler for private messages with media files
@StreamBot.on_message(
    (filters.private) & (filters.document | filters.video | filters.audio | filters.photo), group=4
)
async def private_receive_handler(c: Client, m: Message):
    # Check if the user exists in the database, if not, add the user
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        # Send a message to the bin channel when a new user joins
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined! : \n\n Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!",
        )

    # Check if the updates channel is set and the user is a member of the channel
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            # If the user is kicked from the channel, send a message and return
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="You are banned!\n\n  **C
