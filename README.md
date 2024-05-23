# Web Scraping Project
This project demonstrates web scraping using two different approaches:

- Python's Scrapy framework
- Python's BeautifulSoup library


## Overview
The goal is to scan a given website in parallel and generate a report with the following information:

1. A list of all the links under the given website and their depth
2. A list of all the broken links.


## Requirements
- Python 3.X
- Scrapy - https://scrapy.org/
- Beautiful Soup - https://www.crummy.com/software/BeautifulSoup/
- Other requiremens: check the "requirements.txt" file


# Windows installation

    python -m venv .\.venv
    .venv\Scripts\activate
    pip install -r requirements.txt

# Execution
    .venv\Scripts\activate
    cd site_reporter
    python .\run_report.py

## Executing the spider only
    .venv\Scripts\activate
    cd site_reporter
    scrapy crawl follow_all -o follow.1.json


# Todo
- Fix the error: AttributeError: 'IgnoreRequest' object has no attribute 'response'
