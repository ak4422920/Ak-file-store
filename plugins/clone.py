import re
import requests

from pyrogram import Client, filters

from clone_manager import start_clone, stop_clone
from clone_system.clone_db import add_clone, get_clone, delete_clone

TOKEN_PATTERN = r"\d{8,10}:[a-zA-Z0-9_-]{35}"


@Client.on_message(filters.command("clone") & filters.private)
async def clone(client, message):

    await message.reply(
        "Send your BOT_TOKEN from @BotFather"
    )


@Client.on_message(filters.private & filters.text)
async def receive_token(client, message):

    token = message.text.strip()

    if not re.match(TOKEN_PATTERN, token):
        return

    r = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()

    if not r["ok"]:
        return await message.reply("Invalid BOT_TOKEN")

    username = r["result"]["username"]

    user_id = message.from_user.id

    await add_clone(user_id, token, username)

    await start_clone(token, user_id)

    await message.reply(
        f"✅ Clone Bot Started\n\nBot: @{username}"
    )


@Client.on_message(filters.command("myclone"))
async def myclone(client, message):

    data = await get_clone(message.from_user.id)

    if not data:
        return await message.reply("You don't have a clone.")

    await message.reply(
        f"Your Clone Bot: @{data['username']}"
    )


@Client.on_message(filters.command("deleteclone"))
async def deleteclone(client, message):

    user_id = message.from_user.id

    await stop_clone(user_id)

    await delete_clone(user_id)

    await message.reply("Clone deleted.")
