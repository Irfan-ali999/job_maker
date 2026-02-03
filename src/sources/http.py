from __future__ import annotations

import contextlib
from typing import Optional

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.config import REQUEST_TIMEOUT, USER_AGENT


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.text


def fetch_html_js(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=REQUEST_TIMEOUT * 1000)
        content = page.content()
        context.close()
        browser.close()
        return content


def soup_from_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


@contextlib.contextmanager
def safe_playwright(url: str) -> Optional[str]:
    try:
        yield fetch_html_js(url)
    except Exception:
        yield None
