from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from src.config import SourceConfig
from src.models import Job
from src.sources.http import fetch_html, fetch_html_js, soup_from_html
from src.utils import hash_url, normalize_text, parse_date


class LinkSource:
    def __init__(self, config: SourceConfig) -> None:
        self.config = config

    def fetch(self) -> list[Job]:
        html = fetch_html_js(self.config.url) if self.config.render_js else fetch_html(self.config.url)
        soup = soup_from_html(html)
        return self._parse_links(soup)

    def _parse_links(self, soup: BeautifulSoup) -> list[Job]:
        jobs: list[Job] = []
        for anchor in soup.find_all("a"):
            href = anchor.get("href")
            if not href:
                continue
            text = normalize_text(anchor.get_text(" "))
            if not text:
                continue
            url = urljoin(self.config.url, href)
            job_id = hash_url(url)
            jobs.append(
                Job(
                    id=job_id,
                    title=text,
                    company=self.config.name,
                    sector=self.config.sector,
                    type="job",
                    domain="IT",
                    location="India" if self.config.country == "india" else "",
                    country=self.config.country,
                    remote=False,
                    posted_date=parse_date(text),
                    apply_url=url,
                    source=self.config.name,
                )
            )
        return jobs
