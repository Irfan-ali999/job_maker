from __future__ import annotations

from src.config import (
    APPRENTICESHIP_KEYWORDS,
    DATA_ENTRY_KEYWORDS,
    IT_KEYWORDS,
    NEGATIVE_KEYWORDS,
)
from src.models import Job
from src.utils import contains_any, normalize_text


def classify_domain(title: str) -> str:
    title = normalize_text(title).lower()
    if contains_any(title, DATA_ENTRY_KEYWORDS):
        return "Data Entry"
    return "IT"


def is_apprenticeship(title: str) -> bool:
    return contains_any(title.lower(), APPRENTICESHIP_KEYWORDS)


def has_negative_keyword(title: str) -> bool:
    return contains_any(title.lower(), NEGATIVE_KEYWORDS)


def matches_it(title: str) -> bool:
    return contains_any(title.lower(), IT_KEYWORDS)


def passes_filters(job: Job) -> bool:
    title = job.title.lower()

    if has_negative_keyword(title):
        return False

    if job.sector in {"government", "bank"}:
        if job.country != "india":
            return False

    if job.type == "apprenticeship" and not matches_it(title):
        return False

    if job.domain == "Data Entry":
        return job.remote is True

    if job.sector == "remote":
        # Remote must be explicitly remote for Java Developer or Data Entry Operator.
        is_java = "java" in title
        is_data_entry = contains_any(title, DATA_ENTRY_KEYWORDS)
        return job.remote is True and (is_java or is_data_entry)

    return matches_it(title)
