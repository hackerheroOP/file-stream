# (c) @biisal, Adarsh Goel
# Initalizes and runs the StreamBot

import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import Client as StreamBot
from pyrogram.errors import LoginRequired
from .vars import Var
from .server import web_server
from .utils.keepalive import ping_server

LOGO = """
 ____ ___ ___ ____    _    _    
| __ )_ _|_ _/ ___|  / \  | |   
|  _ \| | | |\___ \ / _ \ | |   
| |_) | | | | ___) / ___ \| |___
|____/___|___|____/_/   \_\_____|"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

async def import_plugins():
    """Import all plugins from the plugins directory."""
    plugins_dir = Path("biisal/bot/plugins")
    plugins = [f.stem for f in plugins_dir.glob("*.py") if f.is_file()]
    for plugin in plugins:
        try:
            importlib.import_module(f".plugins.{plugin}", package="biisal.bot")
            print(f"Imported => {plugin}")
        except Exception as e:
            logging.error(f"Error importing plugin {plugin}: {e}")

async def start_bot():
    """Start the Telegram bot."""
    try:
        bot_info = await StreamBot.get_me()
        StreamBot.username = bot_info.username
    except LoginRequired:
        logging.error("Failed to login to Telegram")
        sys.exit(1)

async def start_services():
    """Start all services."""
    print('\n')
    print('------------------- Initalizing Telegram Bot -------------------')
    await start_bot()
    print("------------------------------ DONE ------------------------------")
    print()
    print('---------------------- Initializing Clients ----------------------')
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    print('\n')
    print('--------------------------- Importing ---------------------------')
    await import_plugins()
    print('------------------------------ DONE ------------------------------')
    print('\n')
    if Var.ON_HEROKU:
        print("------------------ Starting Keep Alive Service ------------------")
        print()
        asyncio.create_task(ping_server())
    print('-------------------- Initalizing Web Server -------------------------')
    app = await web_server()
    await app.start()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, bind_address, Var.PORT)
    print(f'-------------------- Server started at http://{bind_address}:{Var.PORT} --------------------')
    print('\n')
    print('---------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------------------------------------------------------------------')
    print(' follow me for more such exciting bots! https://github.com/biisal')
    print('---------------------------------------------------------------------------------------------------------')
    print('\n')
    print('----------------------- Service Started -----------------------------------------------------------------')
    print('                        bot =>> {}'.format(StreamBot.username))
    print('                        server ip =>> {}:{}'.format(bind_address, Var.PORT))
    print('                        Owner =>> {}'.format(Var.OWNER_USERNAME))
    if Var.ON_HEROKU:
        print('                        app runnng on =>> {}'.format(Var.FQDN))
    print('---------------------------------------------------------------------------------------------------------')
    print(LOGO)
    if Var.OWNER_ID:
        try:
            await StreamBot.send_message(chat_id=Var.OWNER_ID[0], text='<b>ᴊᴀɪ sʜʀᴇᴇ ᴋʀɪsʜɴᴀ 😎\nʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ !!</b>')
        except Exception as e:
            logging.error(f'got this err to send restart msg to owner : {e}')
    await idle()

if __name__ == '__main__':
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopped -----------------------')
