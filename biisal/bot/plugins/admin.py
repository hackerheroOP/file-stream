# (c) @adarsh-goel
# (c) @biisal
import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
import logging
from typing import List, Dict, Tuple, Union

import pyrogram
from pyrogram.types import Message
from biisal.utils.broadcast_helper import send_msg
from biisal.utils.database import Database
from biisal.bot import StreamBot
from biisal.vars import Var

logger = logging.getLogger(__name__)
db = Database(Var.DATABASE_URL, Var.name)
BroadcastIDs = {}

@StreamBot.on_message(filters.command("users") & filters.private)
async def sts(c: Client, m: Message) -> None:
    """
    Reply to the user with the total number of users in the database.
    """
    user_id = m.from_user.id
    if user_id in Var.OWNER_ID:
        total_users = await db.total_users_count()
        await m.reply_text(text=f"Total Users in DB: {total_users}", quote=True)

@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(list(Var.OWNER_ID)))
async def broadcast_(c, m: Message) -> None:
    """
    Initiate a broadcast to all users in the database.
    """
    user_id = m.from_user.id
    out = await m.reply_text(
        text=f"Broadcast initiated! You will be notified with log file when all the users are notified."
    )
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = "".join([random.choice(string.ascii_letters) for i in range(3)])
        if not BroadcastIDs.get(broadcast_id):
            break
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    BroadcastIDs[broadcast_id] = {
        "total": total_users,
        "current": done,
        "failed": failed,
        "success": success,
    }
    try:
        async with aiofiles.open("broadcast.txt", "w") as broadcast_log_file:
            async for user in all_users:
                sts, msg = await send_msg(
                    user_id=int(user["id"]),
                    message=broadcast_msg
                )
                if msg is not None:
                    await broadcast_log_file.write(msg)
                if sts == 200:
                    success += 1
                else:
                    failed += 1
                if sts == 400:
                    await db.delete_user(user["id"])
                done += 1
                if BroadcastIDs.get(broadcast_id) is None:
                    break
                else:
                    BroadcastIDs[broadcast_id].update(
                        {
                            "current": done,
                            "failed": failed,
                            "success": success
                        }
                    )
    except Exception as e:
        logger.error(f"Error during broadcast: {e}")
    else:
        if BroadcastIDs.get(broadcast_id):
            BroadcastIDs.pop(broadcast_id)
        completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
        await asyncio.sleep(3)
        await out.delete()
        if failed == 0:
            await m.reply_text(
                text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
                quote=True
            )
        else:
            await m.reply_document(
                document='broadcast.txt',
                caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
                quote=True
            )
        if os.path.exists('broadcast.txt'):
            os.remove('broadcast.txt')
