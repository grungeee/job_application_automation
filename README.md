# Job Application Automation

## Scraping AMS Job Pages

Use `scraper-project/src/portal_scraper.py` to extract key details from a saved AMS job HTML file.

```bash
python scraper-project/src/portal_scraper.py path/to/file.html
```

The script outputs a JSON object with values from specific HTML element IDs such as `ams-detail-companyname` and `ams-detail-email`.
