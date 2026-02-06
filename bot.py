# bot.py
import asyncio
from pyrogram import Client, idle
from config import CONFIG
from database.connection import CosmicBotz

# Import the web starter function
from web_service import start_web_server

app = Client(
    name="cosmic-bot",
    api_id=CONFIG.API_ID,
    api_hash=CONFIG.API_HASH,
    bot_token=CONFIG.BOT_TOKEN,
    #plugins={"root": "plugins"},
)

async def run_bot():
    print(f"Starting bot @{CONFIG.BOT_USERNAME} ...")
    await CosmicBotz.connect()

    await app.start()
    me = await app.get_me()
    print(f"→ Bot online → @{me.username} (ID: {me.id})")

    await idle()

    await app.stop()
    await CosmicBotz.close()
    print("Bot stopped gracefully")


async def main():
    # Start dummy web server in background (non-blocking)
    web_task = asyncio.create_task(start_web_server())

    # Start bot (this will idle forever until shutdown)
    bot_task = asyncio.create_task(run_bot())

    # Wait for bot task (main control flow)
    await bot_task

    # Cleanup web task on shutdown (rarely reached)
    await web_task


if __name__ == "__main__":
    asyncio.run(main())