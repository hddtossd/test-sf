# WebDirectory – Website Directory & Endpoint Scanner

## Overview
WebDirectory is a modern, responsive web application that scans a given domain for publicly accessible directories, pages, and endpoints. It provides a real‑time dashboard, interactive directory tree, searchable results table, and options to export findings.

## Features
- Domain input with validation and normalization
- Passive discovery via crawling, sitemap, robots.txt, and JS asset analysis
- Optional wordlist‑based directory brute‑forcing (authorized only)
- Real‑time progress UI with statistics cards
- Interactive collapsible directory tree (glassmorphism design, dark theme)
- Search, filter, sort of results
- Export reports to CSV, JSON, TXT, PDF
- Scan history, compare previous scans, pause/resume where supported
- Configurable crawl depth, request timeout, delay, and max URLs

## Technology Stack
**Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript, Chart.js
**Backend**: Python 3.11, FastAPI, `httpx`, `beautifulsoup4`, optional Scrapy
**Database**: SQLite (development) – can be swapped for PostgreSQL

## Project Structure
```
WebDirectory/
├─ backend/
│  ├─ app.py            # FastAPI entry point
│  ├─ scanner.py        # Core scanning engine
│  ├─ crawler.py        # HTML link extraction
│  ├─ sitemap.py        # Sitemap & robots.txt handling
│  ├─ analyzer.py       # Response classification
│  ├─ exporter.py       # CSV/JSON/TXT/PDF exporters
│  ├─ database.py       # SQLite helper
│  └─ requirements.txt
├─ frontend/
│  ├─ index.html
│  ├─ style.css
│  └─ script.js
└─ README.md
```

## Setup & Installation
1. **Clone / download** this repository.
2. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate  # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Run the backend**:
   ```bash
   uvicorn backend.app:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`.
5. **Open the UI**:
   Open `frontend/index.html` in a browser (or serve it via a simple static server).

## Usage
- Enter a domain (e.g., `example.com`) and configure optional settings.
- Click **Start Scan** – the backend will crawl the site respecting robots.txt and rate limits.
- Watch live progress, explore the directory tree, and filter results.
- Export the report when finished.

## Security & Ethics
- Only scan domains you **own** or for which you have **explicit permission**.
- The scanner blocks private IP ranges, localhost, and cloud metadata endpoints.
- No authentication bypass or exploitation is performed; only public resources are accessed.

## License
MIT – feel free to adapt and improve.
