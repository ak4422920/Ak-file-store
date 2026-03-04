from pyrogram import Client, filters


@Client.on_message(filters.command("batch") & filters.private)
async def batch_handler(client, message):

    await message.reply(
        "📦 Send multiple files one by one.\n"
        "When finished, send /done to generate batch link."
    )


@Client.on_message(filters.private & filters.document)
async def collect_files(client, message):

    if not hasattr(client, "batch_files"):
        client.batch_files = {}

    user_id = message.from_user.id

    if user_id not in client.batch_files:
        client.batch_files[user_id] = []

    client.batch_files[user_id].append(message.document.file_id)

    await message.reply("✅ File added to batch.")


@Client.on_message(filters.command("done") & filters.private)
async def finish_batch(client, message):

    user_id = message.from_user.id

    if not hasattr(client, "batch_files") or user_id not in client.batch_files:
        return await message.reply("❌ No batch files found.")

    files = client.batch_files[user_id]

    links = []

    for file in files:
        link = f"https://t.me/{client.username}?start={file}"
        links.append(link)

    text = "📦 Batch Links:\n\n" + "\n".join(links)

    await message.reply(text)

    del client.batch_files[user_id]
