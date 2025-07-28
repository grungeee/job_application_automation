from pathlib import Path
from typing import Dict, Iterable, List

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


DETAIL_IDS = [
    "ams-detail-companyname",
    "ams-detail-location",
    "ams-detail-workingtime",
    "ams-detail-availableFrom",
    "ams-detail-employmentrelationship",
    "ams-detail-source",
    "ams-detail-occupation",
    "ams-detail-education",
    "ams-detail-lastUpdatedAt",
]

CONTACT_IDS = [
    "ams-detail-phone-number-textMobil",
    "ams-detail-phone-number-textFestnetz",
    "ams-detail-email",
]


def _extract_details(soup: BeautifulSoup) -> Dict[str, str]:
    """Return a dictionary of job details from the parsed HTML."""

    def get(id_: str) -> str:
        el = soup.find(id=id_)
        return el.get_text(strip=True) if el else ""

    return {id_: get(id_) for id_ in DETAIL_IDS + CONTACT_IDS}


def scrape_file(html_path: str) -> Dict[str, str]:
    """Extract job details from a saved AMS job page."""
    text = Path(html_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "lxml")
    return _extract_details(soup)


def scrape_url(url: str, *, session: requests.Session | None = None) -> Dict[str, str]:
    """Fetch the job page from `url` and extract details using requests."""
    sess = session or requests.Session()
    resp = sess.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    return _extract_details(soup)


def scrape_url_dynamic(url: str) -> Dict[str, str]:
    """Fetch and render the job page using Playwright and extract details."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto(url, timeout=60000)
        # Wait for a known element to appear to ensure the page has loaded
        page.wait_for_selector("#ams-detail-companyname", timeout=15000)
        soup = BeautifulSoup(page.content(), "lxml")
        browser.close()
        return _extract_details(soup)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Scrape AMS job pages directly from their URLs"
    )
    parser.add_argument("urls", nargs="*", help="Job URLs to scrape")
    parser.add_argument(
        "--urls-file",
        default="urls.txt",
        help="File containing job URLs (one per line)",
    )
    args = parser.parse_args()

    url_list: List[str] = []
    urls_file = Path(args.urls_file)
    if not urls_file.exists():
        alt = Path(__file__).resolve().parents[1] / args.urls_file
        if alt.exists():
            urls_file = alt
    if urls_file.exists():
        lines = urls_file.read_text(encoding="utf-8").splitlines()
        url_list.extend([l.strip() for l in lines if l.strip()])
    url_list.extend(args.urls)

    if not url_list:
        parser.error("No URLs provided")

    results = []
    for url in url_list:
        details = scrape_url_dynamic(url)
        details["url"] = url
        results.append(details)

    print(json.dumps(results, indent=2, ensure_ascii=False))
