from pyrogram import Client, filters
from pyrogram.types import Message
from config import CONFIG
from database.operations.files import get_file_by_code
from bot import app


@app.on_message(filters.private & filters.command("start"))
async def start_or_file_link(client: Client, message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) == 1:
        # plain /start
        first = message.from_user.first_name or "there"
        text = CONFIG.START_MESSAGE.format(first_name=first)
        await message.reply_text(text)
        return

    # /start <code>
    short_code = args[1].strip()

    file_data = await get_file_by_code(short_code)

    if not file_data:
        await message.reply_text("Invalid or expired link.")
        return

    try:
        await client.send_cached_media(
            chat_id=message.chat.id,
            file_id=file_data["file_id"],
            caption=file_data.get("caption", "File from Cosmic Bot 🌌"),
            protect_content=file_data.get("protect_content", True),
            reply_to_message_id=message.id,
        )
    except Exception as e:
        await message.reply_text(f"Cannot send file right now.\n{str(e)}")