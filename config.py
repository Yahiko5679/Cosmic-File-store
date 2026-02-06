from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    API_ID: int = int(os.getenv("API_ID", ""))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    DB_NAME: str = "CosmicFileBotz"

    DB_CHANNEL: int = int(os.getenv("DB_CHANNEL", ""))
    ADMINS: List[int] = [
        int(x.strip()) for x in os.getenv("ADMINS", "").split(",") if x.strip().isdigit()
    ]

    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "CosmicFileBot").lstrip("@")

    START_MESSAGE: str = (
        "Hello {first_name} ✨\n"
        "I am Cosmic File Bot 🌌\n"
        "Send me any file → get permanent shareable link!"
    )

    # You can add later
    PROTECT_CONTENT: bool = False

    def validate(self):
        errors = []
        if self.API_ID == 0:
            errors.append("API_ID missing or invalid")
        if not self.API_HASH:
            errors.append("API_HASH missing")
        if not self.BOT_TOKEN:
            errors.append("BOT_TOKEN missing")
        if not self.MONGODB_URI:
            errors.append("MONGODB_URI missing")
        if self.DB_CHANNEL == 0:
            errors.append("DB_CHANNEL missing or invalid")
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))


CONFIG = Config()
CONFIG.validate()