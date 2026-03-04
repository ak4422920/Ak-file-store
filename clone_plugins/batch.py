from pyrogram import Client, filters
from pyrogram.types import Message
import random
import string

BATCH_DB = {}


def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


@Client.on_message(filters.command("batch") & filters.private)
async def batch_start(client: Client, message: Message):

    await message.reply(
        "Send the **first post link** from the channel."
    )

    client.batch_step = {}
    client.batch_step[message.from_user.id] = "FIRST"


@Client.on_message(filters.private & filters.text)
async def batch_handler(client: Client, message: Message):

    if not hasattr(client, "batch_step"):
        return

    user_id = message.from_user.id

    if user_id not in client.batch_step:
        return

    step = client.batch_step[user_id]

    if step == "FIRST":

        try:
            first = int(message.text.split("/")[-1])
        except:
            return await message.reply("Invalid link. Send again.")

        client.batch_first = first
        client.batch_step[user_id] = "LAST"

        return await message.reply(
            "Now send the **last post link**."
        )

    if step == "LAST":

        try:
            last = int(message.text.split("/")[-1])
        except:
            return await message.reply("Invalid link.")

        first = client.batch_first

        if last < first:
            return await message.reply("Last link must be greater.")

        key = generate_key()

        BATCH_DB[key] = (first, last)

        link = f"https://t.me/{client.username}?start=batch_{key}"

        del client.batch_step[user_id]

        await message.reply(
            f"📦 Batch Link Generated:\n\n{link}"
        )
