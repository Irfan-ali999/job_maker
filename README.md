# Automated IT Job Monitor (GitHub Actions)

This repo runs a fully automated, cloud-hosted job monitor using GitHub Actions. It scrapes approved sources, filters by IT rules, deduplicates results, and sends Telegram notifications only when **new** opportunities appear.

## What it covers
- **Government + Bank (India only)**: SBI, RBI, NABARD, IBPS pages.
- **Private + Remote**: RemoteOK API, WeWorkRemotely RSS, optional Greenhouse/Lever ATS boards.
- **Remote constraint**: Only **Remote Java Developer** and **Remote Data Entry Operator** roles.

## How it runs
- **IT & Remote pipeline**: every 6 hours.
- **Government & Bank pipeline**: once daily.

## Setup
### 1) GitHub Secrets
Create these repository secrets:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### 2) Optional ATS sources (Fortune 100 / Big 4 / mass hiring / auto companies)
Edit `src/config.py` and add company slugs:
- `GREENHOUSE_COMPANIES = ["company-slug"]`
- `LEVER_COMPANIES = ["company-slug"]`

Example:
```python
GREENHOUSE_COMPANIES = ["github", "asana"]
LEVER_COMPANIES = ["netflix"]
```

### 3) GitHub Actions
Workflows are already configured:
- `.github/workflows/it-remote.yml`
- `.github/workflows/gov-bank.yml`

## Data persistence
`data/seen.db` stores hashes of seen jobs. The workflows auto-commit this file so the system keeps state between runs.

## Local (optional) dry run
You do **not** need Python locally to run production. If you want a quick local test:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python -m src.main --pipeline it-remote
```

## Notes
- Filters enforce **IT-only** and **remote-only** for data entry.
- Apprenticeships are only included if IT keywords are present.
