# Job Application Automation

## Scraping AMS Job Pages

Use `scraper-project/src/portal_scraper.py` to scrape AMS job postings directly from their URLs. The script relies on Playwright to render the pages.

Add job links to `urls.txt` (one URL per line) or pass them on the command line. The script prints a JSON array with values from HTML IDs such as `ams-detail-companyname` and `ams-detail-email`.

```bash
# install dependencies and browser
pip install -r scraper-project/requirements.txt
playwright install chromium
# on Linux you may also need system packages
playwright install-deps chromium

# scrape URLs listed in urls.txt
python scraper-project/src/portal_scraper.py

# or scrape a specific URL
python scraper-project/src/portal_scraper.py "https://jobs.ams.at/public/emps/jobs/uuid/..."
```
