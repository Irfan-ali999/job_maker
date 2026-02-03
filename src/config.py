from __future__ import annotations

from dataclasses import dataclass
from typing import List

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

REQUEST_TIMEOUT = 25

IT_KEYWORDS = [
    "software",
    "developer",
    "software engineer",
    "it",
    "information technology",
    "java",
    "java developer",
    "spring",
    "spring boot",
    "data",
    "data analyst",
    "data engineer",
    "data scientist",
    "ai",
    "ml",
    "machine learning",
    "cloud",
    "aws",
    "azure",
    "gcp",
    "devops",
    "cybersecurity",
    "security",
    "network engineer",
    "system administrator",
    "full stack",
    "backend",
    "frontend",
    "python",
    "javascript",
    "c++",
    "web developer",
    "mobile app",
    "qa",
    "automation testing",
    "embedded software",
]

DATA_ENTRY_KEYWORDS = [
    "data entry",
    "data entry operator",
    "data processing",
]

APPRENTICESHIP_KEYWORDS = [
    "apprentice",
    "apprenticeship",
    "trainee",
]

NEGATIVE_KEYWORDS = [
    "mechanical",
    "civil",
    "electrical",
    "manufacturing",
    "production",
    "plant",
    "automobile technician",
    "hr",
    "finance",
    "accounting",
    "marketing",
    "sales",
    "operations",
]


@dataclass(frozen=True)
class SourceConfig:
    name: str
    url: str
    sector: str
    country: str
    render_js: bool = False


REMOTE_SOURCES: List[SourceConfig] = [
    SourceConfig(
        name="RemoteOK",
        url="https://remoteok.com/api",
        sector="remote",
        country="global",
    ),
    SourceConfig(
        name="WeWorkRemotely",
        url="https://weworkremotely.com/categories/remote-programming-jobs.rss",
        sector="remote",
        country="global",
    ),
]

GOV_BANK_SOURCES: List[SourceConfig] = [
    SourceConfig(
        name="SBI",
        url="https://sbi.co.in/web/careers",
        sector="bank",
        country="india",
    ),
    SourceConfig(
        name="RBI",
        url="https://www.rbi.org.in/Scripts/BS_ViewAllNotifications.aspx",
        sector="bank",
        country="india",
        render_js=True,
    ),
    SourceConfig(
        name="NABARD",
        url="https://www.nabard.org/content1.aspx?id=1903&catid=23&mid=23",
        sector="bank",
        country="india",
    ),
    SourceConfig(
        name="IBPS",
        url="https://www.ibps.in/career/",
        sector="bank",
        country="india",
        render_js=True,
    ),
]

# Optional: add ATS company boards here.
# Example entries:
# GREENHOUSE_COMPANIES = ["company-slug"]  # https://boards.greenhouse.io/company-slug
# LEVER_COMPANIES = ["company-slug"]  # https://jobs.lever.co/company-slug
GREENHOUSE_COMPANIES: List[str] = []
LEVER_COMPANIES: List[str] = []
