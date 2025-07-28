from pathlib import Path
from typing import Dict

from bs4 import BeautifulSoup


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


def scrape_details(html_path: str) -> Dict[str, str]:
    """Extract job details from a saved AMS job page."""
    text = Path(html_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "lxml")

    def get(id_: str) -> str:
        el = soup.find(id=id_)
        return el.get_text(strip=True) if el else ""

    data: Dict[str, str] = {}
    for id_ in DETAIL_IDS + CONTACT_IDS:
        data[id_] = get(id_)
    return data


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scrape saved AMS job HTML file")
    parser.add_argument("html", help="Path to the downloaded HTML file")
    args = parser.parse_args()

    results = scrape_details(args.html)
    print(json.dumps(results, indent=2, ensure_ascii=False))
