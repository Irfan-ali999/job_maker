from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Job:
    id: str
    title: str
    company: str
    sector: str
    type: str
    domain: str
    location: str
    country: str
    remote: bool
    posted_date: Optional[str]
    apply_url: str
    source: str
