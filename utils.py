import base64
import hashlib
from typing import Any
from config import API_KEY, MERCHANT_UUID


def generate_signature(data: str) -> str:
    return hashlib.md5(base64.b64encode(data.encode()) + API_KEY.encode()).hexdigest()


def generate_headers(data: str) -> dict[str, Any]:
    return {
        "merchant": MERCHANT_UUID,
        "sign": generate_signature(data),
        "Content-Type": "application/json"
    }