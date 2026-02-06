from database.connection import CosmicBotz
from typing import Optional, Dict, Any
import time


async def save_file_metadata(
    short_code: str,
    file_id: str,
    file_unique_id: str,
    user_id: int,
    file_name: Optional[str] = None,
    mime_type: Optional[str] = None,
    caption: str = "",
    protect_content: bool = True,
) -> None:
    collection = CosmicBotz.get_collection("files")

    document = {
        "_id": short_code,
        "file_id": file_id,
        "file_unique_id": file_unique_id,
        "user_id": user_id,
        "file_name": file_name,
        "mime_type": mime_type,
        "caption": caption,
        "protect_content": protect_content,
        "created_at": int(time.time()),
    }

    await collection.insert_one(document)


async def get_file_by_code(short_code: str) -> Optional[Dict[str, Any]]:
    collection = CosmicBotz.get_collection("files")
    return await collection.find_one({"_id": short_code})