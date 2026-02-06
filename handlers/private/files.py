from pyrogram import Client, filters
from pyrogram.types import Message
from config import CONFIG
from utils.short_code import generate_short_code
from database.operations.files import save_file_metadata


media_filter = (
    filters.document
    | filters.video
    | filters.audio
    | filters.photo
    | filters.voice
    | filters.animation
)


@app.on_message(filters.private & media_filter)
async def handle_incoming_file(client: Client, message: Message):
    user = message.from_user
    if not user:
        await message.reply("Cannot identify user.")
        return

    media = (
        message.document
        or message.video
        or message.audio
        or message.photo
        or message.voice
        or message.animation
    )

    if not media:
        return

    try:
        forwarded = await client.copy_message(
            chat_id=CONFIG.DB_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id,
            disable_notification=True,
        )
    except Exception as e:
        await message.reply(f"Failed to save file:\n{str(e)}")
        return

    # Prefer document/video file_id from forwarded message
    saved_file_id = getattr(forwarded.document or forwarded.video or forwarded.photo or forwarded.animation, "file_id", None)
    if not saved_file_id:
        await message.reply("Could not get permanent file_id.")
        return

    short_code = generate_short_code(user.id, media.file_unique_id)

    await save_file_metadata(
        short_code=short_code,
        file_id=saved_file_id,
        file_unique_id=media.file_unique_id,
        user_id=user.id,
        file_name=media.file_name,
        mime_type=media.mime_type,
        caption=message.caption or "",
        protect_content=CONFIG.PROTECT_CONTENT,
    )

    link = f"https://t.me/{CONFIG.BOT_USERNAME}?start={short_code}"

    await message.reply_text(
        f"**File stored!**\n\n"
        f"Share link:\n`{link}`\n\n"
        f"Anyone with this link can download the file.",
        disable_web_page_preview=True
    )