from motor.motor_asyncio import AsyncIOMotorClient
from config import CONFIG
from typing import Optional


class Database:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.connected = False

    async def connect(self):
        if self.connected:
            return

        try:
            self.client = AsyncIOMotorClient(CONFIG.MONGODB_URI)
            self.db = self.client[CONFIG.DB_NAME]
            await self.db.command("ping")
            print(f"→ MongoDB connected | DB: {CONFIG.DB_NAME}")
            self.connected = True
        except Exception as e:
            print(f"→ MongoDB connection failed: {str(e)}")
            raise

    async def close(self):
        if self.client and self.connected:
            self.client.close()
            print("→ MongoDB connection closed")
            self.connected = False

    def get_collection(self, name: str):
        if not self.connected or self.db is None:
            raise RuntimeError("Database not connected. Call await CosmicBotz.connect() first.")
        return self.db[name]


CosmicBotz = Database()