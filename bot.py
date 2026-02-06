import asyncio
from pyrogram import Client, idle, filters
from config import CONFIG
from database.connection import CosmicBotz

app = Client(
    name="cosmic-bot",
    api_id=CONFIG.API_ID,
    api_hash=CONFIG.API_HASH,
    bot_token=CONFIG.BOT_TOKEN,
    plugins=dict(root="handlers"),
)

@app.on_message(filters.private & filters.command("start") & ~filters.regex(r"^/start .+"))
async def basic_start(client, message):
    first = message.from_user.first_name or "there"
    text = CONFIG.START_MESSAGE.format(first_name=first)
    await message.reply_text(text)


async def main():
    print(f"Starting @{CONFIG.BOT_USERNAME} ...")
    await CosmicBotz.connect()

    await app.start()
    me = await app.get_me()
    print(f"→ Bot online → @{me.username} (ID: {me.id})")

    await idle()

    await app.stop()
    await CosmicBotz.close()
    print("Bot stopped gracefully")


if __name__ == "__main__":
    asyncio.run(main())