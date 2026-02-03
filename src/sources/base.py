from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from src.models import Job


class BaseSource(ABC):
    name: str

    @abstractmethod
    def fetch(self) -> List[Job]:
        raise NotImplementedError
