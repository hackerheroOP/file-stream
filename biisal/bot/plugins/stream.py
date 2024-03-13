# (c) Adarsh-Goel
# (c) @biisal
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

# from utils_bot import get_shortlink

from biisal.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")

msg_text = """<b>‣ ʏᴏᴜʀ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ! 😎

‣ Fɪʟᴇ ɴᴀᴍᴇ : <i>{}</i>
‣ Fɪʟᴇ ꜱɪᴢᴇ : {}

🔻 <a href="{}">𝗙𝗔𝗦𝗧 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗</a>
🔺 <a href="{}">𝗪𝗔𝗧𝗖𝗛 𝗢𝗡𝗟𝗜𝗡𝗘</a>

‣ ɢᴇᴛ <a href="https://t.me/movies_desire_bot">ᴍᴏʀᴇ ғɪʟᴇs</a></b> 🤡""\"
"""

@StreamBot.on_message(
    (filters.private) & (filters.document | filters.video | filters.audio | filters.photo), group=4
)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined! : \n\n Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!",
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="You are banned!\n\n  **Cᴏɴᴛᴀᴄᴛ Support [Support](https://t.me/pro_morningstar) They Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**}",
                    disable_web_page_preview=True,
                )
                return
        except UserNotParticipant:
            await c.send_photo(
                chat_id=m.chat.id,
                photo="https://telegra.ph/file/ad5d6fbbaf1ed157d8a8d.jpg",
                caption="""<b>Hᴇʏ ᴛʜᴇʀᴇ!\n\nPʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ ! 😊\n\nDᴜᴇ ᴛᴏ sᴇʀᴠᴇʀ ᴏᴠᴇʀʟᴏᴀᴅ, ᴏɴʟʏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ !</b>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🚩", url=f"https://t.me/{Var.UPDATES_CHANNEL}"]
                        ]
                    ]
                ),
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ Support** [Support](https://t.me/pro_morningstar_bot)",
                disable_web_page_preview=True,
            )
            return
    ban_chk = await db.is_banned(int(m.from_user.id))
    if ban_chk == True:
        return await m.reply(Var.BAN_ALERT)
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

        await log_msg.reply_text(
            text=f"**Rᴇǫᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}
