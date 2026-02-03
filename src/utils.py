from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Optional

from dateutil import parser


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def parse_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        parsed = parser.parse(value, fuzzy=True)
        return parsed.date().isoformat()
    except (parser.ParserError, ValueError):
        return None


def contains_any(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)
