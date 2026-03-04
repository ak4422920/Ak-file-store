from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start(client, message):

    await message.reply(
        "Hello! Send me a file and I will generate a link."
    )
