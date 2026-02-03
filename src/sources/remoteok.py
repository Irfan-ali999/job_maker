from __future__ import annotations

import requests

from src.config import REQUEST_TIMEOUT, USER_AGENT
from src.models import Job
from src.utils import hash_url, normalize_text, parse_date


class RemoteOKSource:
    name = "RemoteOK"

    def fetch(self) -> list[Job]:
        response = requests.get(
            "https://remoteok.com/api",
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()

        jobs: list[Job] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            if item.get("id") in (None, 0):
                continue
            url = item.get("url")
            if not url:
                continue
            title = normalize_text(item.get("position", ""))
            company = normalize_text(item.get("company", "")) or "RemoteOK"
            location = normalize_text(item.get("location", "")) or "Remote"
            posted = parse_date(item.get("date"))
            job_id = hash_url(url)

            jobs.append(
                Job(
                    id=job_id,
                    title=title,
                    company=company,
                    sector="remote",
                    type="job",
                    domain="IT",
                    location=location,
                    country="global",
                    remote=True,
                    posted_date=posted,
                    apply_url=url,
                    source=self.name,
                )
            )

        return jobs
