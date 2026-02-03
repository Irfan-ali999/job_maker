from __future__ import annotations

import os
from typing import Iterable

import requests

from src.models import Job


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str) -> None:
        response = requests.post(
            self.api_url,
            json={"chat_id": self.chat_id, "text": message, "disable_web_page_preview": True},
            timeout=20,
        )
        response.raise_for_status()

    def notify_jobs(self, jobs: Iterable[Job]) -> None:
        for job in jobs:
            message = (
                f"{job.title}\n"
                f"{job.company}\n"
                f"Sector: {job.sector} | Type: {job.type} | Domain: {job.domain}\n"
                f"Location: {job.location} | Remote: {job.remote}\n"
                f"Posted: {job.posted_date or 'Unknown'}\n"
                f"Apply: {job.apply_url}"
            )
            self.send(message)


def build_notifier_from_env() -> TelegramNotifier:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
    return TelegramNotifier(token=token, chat_id=chat_id)
