# (c) @biisal, adarsh-goel
import asyncio
import traceback
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

MAX_RETRIES = 5

async def send_msg(user_id, message):
    if not user_id or not message:
        return 400, "Invalid arguments"
    
    retries = 0
    
    while True:
        try:
            await message.forward(chat_id=user_id)
            return 200, None
        except FloodWait as e:
            if retries >= MAX_RETRIES:
                return 500, f"{user_id} : FloodWait exceeded the maximum number of retries\n"
            
            await asyncio.sleep(e.x)
            retries += 1
        except InputUserDeactivated:
            return 400, f"{user_id} : deactivated\n"
        except UserIsBlocked:
            return 400, f"{user_id} : blocked the bot\n"
        except PeerIdInvalid:
            return 400, f"{user_id} : user id invalid\n"
        except Exception as e:
            return 500, f"{user_id} : {traceback.format_exc()}\n"
