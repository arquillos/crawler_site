# Web Scraping Project
This project demonstrates web scraping using two different approaches:

- Python's Scrapy framework
- Python's BeautifulSoup library (WIP)

The website used to test the project is:
- https://crawler-test.com


---
# Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Windows installation](#windows-installation)
4. [Project execution](#project-execution)
5. [To do](#todo)

---
## Overview
The goal is to scan a given website in parallel and generate a report with the following information:

1. A list of all the links under the given website and their depth
2. A list of all the broken links.

---
## Requirements
- Python 3.X
- Scrapy - https://scrapy.org/
- Beautiful Soup - https://www.crummy.com/software/BeautifulSoup/
- Other requiremens: check the "requirements.txt" file

---
# Windows installation
    python -m venv .\.venv
    .venv\Scripts\activate
    pip install -r requirements.txt

# Project execution

## Scrapy
    .venv\Scripts\activate
    cd site_reporter
    python .\run_report.py

### Executing the spider only
    .venv\Scripts\activate
    cd site_reporter
    scrapy crawl follow_all -o follow.1.json

## BeautifulSoup
    .venv\Scripts\activate
    cd .\beautifulsoup_project
    python .\crawler.py

---
# Todo
- The "BeautifulSoup" projet is not finished:
  - There is no limit to the number of asynchronous connections. This can be implemented in several ways:
    - aiohttp.TCPConnector(limit=X)
    - asyncio.Semaphore
    - ...
 - Improve the exception handling
 - Fix the error

        UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

