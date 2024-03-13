# (c) biisal (c) adarsh-goel
import os

from pyrogram import Client
from pyromod.listen import Listen
from ...vars import Var

StreamBot = Client(
    name="Web Streamer",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS,
)

multi_clients = {}
work_loads = {}

# Add some useful functions to manage the workloads
def add_workload(client, workload):
    work_loads[client] = workload

def get_workload(client):
    return work_loads.get(client, None)

def remove_workload(client):
    if client in work_loads:
        del work_loads[client]

# Add a listener to handle new messages
@StreamBot.on_message()
async def handle_message(client, message):
    # Do something with the message here
    pass

# Start the bot
if __name__ == "__main__":
    print(f"Starting bot in {os.getcwd()}")
    StreamBot.run()
