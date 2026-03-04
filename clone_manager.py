from pyrogram import Client
from config import API_ID, API_HASH

running_clones = {}

async def start_clone(token, user_id):

    clone = Client(
        f"clone_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=token,
        plugins={"root": "clone_plugins"}
    )

    await clone.start()

    running_clones[user_id] = clone


async def stop_clone(user_id):

    if user_id in running_clones:
        await running_clones[user_id].stop()
        del running_clones[user_id]
