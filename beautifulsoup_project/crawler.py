"""Module documentation pending"""
import asyncio
import logging

from itertools import chain

import aiohttp
import requests

from aiohttp import ClientConnectorError
from bs4 import BeautifulSoup
from requests import PreparedRequest


# URL to the website
BASE_URL = "https://crawler-test.com"

# Only scrape pages within the domain
ALLOWED_DOMAIN = "crawler-test.com"

# Basic loggin configuration
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


def check_url(url) -> str:
    """A hacky way to check if the URL is valid by using the Requests framework
    """
    prepared_request = PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return prepared_request.url
    except (requests.exceptions.MissingSchema, Exception):
        return ""


def is_url_in_the_domain(url :str) -> bool:
    """Avoid the URLs from another websites"""
    return ALLOWED_DOMAIN in url


async def get_page_html(page_url: str) -> str:
    """Get the page HTML code asynchronously"""

    # Step 1: Filter out the pages not in the domain
    if not is_url_in_the_domain(page_url):
        logging.warning("Skipping, out of allowed domain (%s)", page_url)
        return ""

    # Step 2: Get the page url
    if check_url(page_url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as client:
            try:
                async with client.get(page_url) as resp:
                    return await resp.text() if (resp.status == 200) else ""
            except ClientConnectorError:
                logging.warning("Impossible to connect: %s", page_url)
                return ""
            except aiohttp.client_exceptions.TooManyRedirects:
                logging.warning("Too many redirections: %s", page_url)
                return ""
            except UnicodeDecodeError:
                logging.warning("Unidecode error: %s", page_url)
                return ""
    else:
        logging.warning("Invalid URL: %s", page_url)
        return ""


def get_links_from_html(page_html: str) -> list[str]:
    """Get the likns from a HTML doc"""
    soup = BeautifulSoup(page_html, "lxml")
    links = []
    for link in soup.findAll("a"):
        links.append(f"{BASE_URL}{link.get('href')}")
    return links


def is_duplicated(original_links, link) -> bool:
    """Check if a link has been browsed before"""
    for original_link in original_links:
        if original_link["url"] == link:
            return True
    return False


def add_new_links(original_links, new_links, depth) -> list[dict]:
    """"Add all the new links to browse"""
    for link in new_links:
        if not is_duplicated(original_links, link):
            original_links.append(
                {
                    "url": link,
                    "depth": depth,
                }
            )
    return original_links


async def scrape(page_url: str, depth: int) -> list[dict]:
    """Srape a web page"""
    logging.debug("Processing the page: %s with depth %d", page_url, depth)
    links_list = [
        {
            "url": page_url,
            "depth": depth,
            "error": False
        }
    ]

    # Step 1: Get the links form the page
    page_html: str = await get_page_html(page_url)

    # The link is not valid for browsing
    if page_html == "" or page_html is None:
        links_list[0]["error"] = True
        return links_list

    links: list[str] = get_links_from_html(page_html)

    # Step 2: Update the result
    links_list = add_new_links(links_list, links, depth)

    # Step 4: Recursive parsing
    coros = [scrape(new_link["url"], depth + 1) for new_link in links_list]
    new_links_found = await asyncio.gather(*coros)

    # Step 5: Update the result
    links_list = add_new_links(links_list, chain(*new_links_found), depth)

    # Step 6: Eliminate duplicates
    return links_list


def print_header(header: str) -> None:
    """Print a header"""
    print("-----------------")
    print(f"- {header} -")
    print("-----------------")


def print_links_with_depth(dictionaries: list[dict]) -> None:
    """Print all the links and the depth"""
    print_header("All the links")
    for link in dictionaries:
        print(f"link: {link["url"]} - Depth: {link["depth"]}")
    print("-----------------\n")


def print_error_links(dictionaries: list[dict]) -> None:
    """Print the links with errors"""
    print_header(" Error links ")
    for link in dictionaries:
        if link["error"]:
            print(f"link: {link["url"]}")
    print("-----------------\n")


if __name__ == "__main__":
    print("----------------------")
    print(f"Scrapping the website: {BASE_URL}")
    print("----------------------")
    dict_result: list[dict] = asyncio.run(scrape(BASE_URL, 1))
    print_links_with_depth(dict_result)
    print_error_links(dict_result)
