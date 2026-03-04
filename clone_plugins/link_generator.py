from pyrogram import Client, filters

@Client.on_message(filters.private & filters.document)
async def link_generator(client, message):

    await message.reply(
        "File received. Generating link..."
    )
