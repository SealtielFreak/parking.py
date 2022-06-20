import json

from typing import Dict, Any


def json_to_dict(body: bytes, decode: str = "utf-8") -> Dict[str, Any]:
    try:
        return json.loads(body.decode(decode))
    except (ValueError, TypeError):
        return {}