from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from src.models import Job


class SeenStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS seen (
                    id TEXT PRIMARY KEY,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT,
                    company TEXT,
                    url TEXT
                )
                """
            )
            conn.commit()

    def is_seen(self, job_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT 1 FROM seen WHERE id = ?", (job_id,))
            return cur.fetchone() is not None

    def mark_seen_many(self, jobs: Iterable[Job]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                "INSERT OR IGNORE INTO seen (id, title, company, url) VALUES (?, ?, ?, ?)",
                [(job.id, job.title, job.company, job.apply_url) for job in jobs],
            )
            conn.commit()
