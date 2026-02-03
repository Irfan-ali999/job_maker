from __future__ import annotations

import argparse
import logging
from typing import Iterable

from src import config
from src.filters import classify_domain, is_apprenticeship, passes_filters
from src.models import Job
from src.notify import build_notifier_from_env
from src.sources.ats import fetch_greenhouse, fetch_lever
from src.sources.link_source import LinkSource
from src.sources.remoteok import RemoteOKSource
from src.sources.weworkremotely import WeWorkRemotelySource
from src.storage import SeenStore


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def enrich_job(job: Job) -> Job:
    domain = classify_domain(job.title)
    job_type = job.type
    if is_apprenticeship(job.title):
        job_type = "apprenticeship"
    elif "intern" in job.title.lower():
        job_type = "internship"

    return Job(
        **{
            **job.__dict__,
            "type": job_type,
            "domain": domain,
        }
    )


def collect_jobs(pipeline: str) -> list[Job]:
    jobs: list[Job] = []
    if pipeline == "it-remote":
        jobs.extend(RemoteOKSource().fetch())
        for source in config.REMOTE_SOURCES:
            if source.name == "WeWorkRemotely":
                jobs.extend(WeWorkRemotelySource(source.url).fetch())

        for company in config.GREENHOUSE_COMPANIES:
            jobs.extend(fetch_greenhouse(company))

        for company in config.LEVER_COMPANIES:
            jobs.extend(fetch_lever(company))

    elif pipeline == "gov-bank":
        for source in config.GOV_BANK_SOURCES:
            jobs.extend(LinkSource(source).fetch())
    else:
        raise ValueError("Unknown pipeline")

    return jobs


def filter_new_jobs(jobs: Iterable[Job], store: SeenStore) -> list[Job]:
    filtered: list[Job] = []
    for job in jobs:
        enriched = enrich_job(job)
        if not passes_filters(enriched):
            continue
        if store.is_seen(enriched.id):
            continue
        filtered.append(enriched)
    return filtered


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", required=True, choices=["it-remote", "gov-bank"])
    parser.add_argument("--db", default="data/seen.db")
    args = parser.parse_args()

    store = SeenStore(args.db)
    logging.info("Fetching sources for pipeline: %s", args.pipeline)
    jobs = collect_jobs(args.pipeline)
    logging.info("Fetched %s items", len(jobs))

    new_jobs = filter_new_jobs(jobs, store)
    if not new_jobs:
        logging.info("No new jobs matched filters")
        return

    notifier = build_notifier_from_env()
    notifier.notify_jobs(new_jobs)
    store.mark_seen_many(new_jobs)
    logging.info("Notified %s new jobs", len(new_jobs))


if __name__ == "__main__":
    main()
