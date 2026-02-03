from __future__ import annotations

import requests

from src.config import REQUEST_TIMEOUT, USER_AGENT
from src.models import Job
from src.utils import hash_url, normalize_text, parse_date


def fetch_greenhouse(company: str) -> list[Job]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()

    jobs: list[Job] = []
    for item in payload.get("jobs", []):
        title = normalize_text(item.get("title", ""))
        link = item.get("absolute_url", "")
        location = normalize_text(item.get("location", {}).get("name", ""))
        posted = parse_date(item.get("updated_at"))
        if not link:
            continue
        jobs.append(
            Job(
                id=hash_url(link),
                title=title,
                company=normalize_text(item.get("company", "")) or company,
                sector="private",
                type="job",
                domain="IT",
                location=location,
                country="global",
                remote="remote" in location.lower(),
                posted_date=posted,
                apply_url=link,
                source="Greenhouse",
            )
        )
    return jobs


def fetch_lever(company: str) -> list[Job]:
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()

    jobs: list[Job] = []
    for item in payload:
        link = item.get("hostedUrl")
        if not link:
            continue
        title = normalize_text(item.get("text", ""))
        location = normalize_text(item.get("categories", {}).get("location", ""))
        posted = parse_date(item.get("createdAt"))
        jobs.append(
            Job(
                id=hash_url(link),
                title=title,
                company=company,
                sector="private",
                type="job",
                domain="IT",
                location=location,
                country="global",
                remote="remote" in location.lower(),
                posted_date=posted,
                apply_url=link,
                source="Lever",
            )
        )
    return jobs
