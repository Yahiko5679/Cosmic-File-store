import hashlib
import time


def generate_short_code(user_id: int, file_unique_id: str) -> str:
    """
    Generates short, collision-resistant code: c-xxxxxxxxxxxx
    """
    seed = f"{user_id}{file_unique_id}{int(time.time() * 1000)}"
    digest = hashlib.sha256(seed.encode()).hexdigest()
    return f"c-{digest[:10]}"


def is_valid_short_code(code: str) -> bool:
    return code.startswith("c-") and len(code) == 12