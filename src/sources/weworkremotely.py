from __future__ import annotations

from src.models import Job
from src.sources.http import fetch_html, soup_from_html
from src.utils import hash_url, normalize_text, parse_date


class WeWorkRemotelySource:
    name = "WeWorkRemotely"

    def __init__(self, url: str) -> None:
        self.url = url

    def fetch(self) -> list[Job]:
        xml = fetch_html(self.url)
        soup = soup_from_html(xml)
        items = soup.find_all("item")
        jobs: list[Job] = []

        for item in items:
            title = normalize_text(item.findtext("title", ""))
            link = item.findtext("link", "")
            if not link:
                continue
            company = "WeWorkRemotely"
            location = "Remote"
            posted = parse_date(item.findtext("pubDate", ""))
            job_id = hash_url(link)
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
                    apply_url=link,
                    source=self.name,
                )
            )
        return jobs
