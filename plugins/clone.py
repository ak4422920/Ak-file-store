import re
import requests
from pyrogram import Client, filters

from clone_manager import start_clone, stop_clone
from clone_system.clone_db import add_clone, get_clone, get_all_clones, delete_clone

TOKEN_PATTERN = r"\d{8,10}:[a-zA-Z0-9_-]{35}"

MAX_CLONES = 200


@Client.on_message(filters.private & filters.regex(TOKEN_PATTERN))
async def clone_command(client, message):

    user_id = message.from_user.id

    data = await get_clone(user_id)

    if data:
        return await message.reply(
            f"⚠️ You already have a clone bot\n\n🤖 @{data['username']}"
        )

    clones = await get_all_clones()

    if len(clones) >= MAX_CLONES:
        return await message.reply(
            "🚫 Clone system is currently full.\nTry again later."
        )

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
        return await message.reply("❌ Invalid BOT_TOKEN")

    username = r["result"]["username"]
    user_id = message.from_user.id

    data = await get_clone(user_id)

    if data:
        return await message.reply(
            f"⚠️ You already have a clone\n\n@{data['username']}"
        )

    clones = await get_all_clones()

    if len(clones) >= MAX_CLONES:
        return await message.reply(
            "🚫 Clone system full"
        )

    await add_clone(user_id, token, username)

    try:
        await start_clone(token, user_id)
    except Exception as e:
        return await message.reply(f"Clone start failed\n{e}")

    await message.reply(
        f"✅ Clone Bot Started Successfully\n\n🤖 @{username}"
    )


@Client.on_message(filters.command("myclone") & filters.private)
async def myclone(client, message):

    data = await get_clone(message.from_user.id)

    if not data:
        return await message.reply("You don't have a clone bot.")

    await message.reply(
        f"🤖 Your Clone Bot\n\n@{data['username']}"
    )


@Client.on_message(filters.command("deleteclone") & filters.private)
async def deleteclone(client, message):

    user_id = message.from_user.id

    data = await get_clone(user_id)

    if not data:
        return await message.reply("No clone found.")

    await stop_clone(user_id)

    await delete_clone(user_id)

    await message.reply(
        "🗑 Clone bot deleted successfully."
    )
