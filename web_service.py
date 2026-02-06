# web_service.py
import os
import asyncio
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Cosmic File Bot – Render Health Check")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Cosmic File Bot is alive"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


async def start_web_server():
    """
    Starts the dummy HTTP server on the PORT provided by Render (or default 10000).
    Runs asynchronously so it doesn't block the bot.
    """
    port = int(os.environ.get("PORT", "8080"))
    host = "0.0.0.0"

    print(f"→ Starting dummy HTTP server on {host}:{port} (for Render health checks)")

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="info",
        factory=False,
    )
    server = uvicorn.Server(config)

    # Run in background (non-blocking for asyncio)
    await server.serve()