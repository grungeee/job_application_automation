"""Micro‑scraper entry point — replace with your own genius."""

from pathlib import Path
import requests
from bs4 import BeautifulSoup

def fetch(url: str, *, session: requests.Session | None = None) -> BeautifulSoup:
    """Pulls HTML from `url` and returns a BeautifulSoup DOM tree."""
    sess = session or requests.Session()
    resp = sess.get(url, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def main():
    demo_url = "https://example.org"
    soup = fetch(demo_url)
    title = soup.select_one("title").text.strip()
    print(f"<title>: {title}")


if __name__ == "__main__":
    main()
