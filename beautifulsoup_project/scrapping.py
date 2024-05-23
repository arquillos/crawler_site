"""Module documentation pending"""
import requests
import re

from bs4 import BeautifulSoup
from requests.models import PreparedRequest


def check_url(url):
    prepared_request = PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return prepared_request.url
    except (requests.exceptions.MissingSchema, Exception):
        print(f"Invalid URL: {url}")
        return ""


def recursiveUrl(base_url, link, depth):
    """Missing method doc"""
    try:
        href: str = link['href']      # get value of the href attribute
    except KeyError:
        print(f"No href in link: {link}")
        return link

    # Avoiding corner cases
    if (href == "/" or href.endswith("#") or "http" in href):
        return link

    # Validating the URL
    url = check_url(base_url + href)
    if url == "":
        return link

    try:
        print(f"Page: {url}")
        page = requests.get(url)
    except requests.RequestException:
        print(f"Exception for: {url}")
        return link

    print(f"Depth: {depth}")
    soup = BeautifulSoup(page.text, 'html.parser')
    newlink = soup.find('a')
    if newlink is None:
        return link
    else:
        return link, recursiveUrl(url, newlink, depth + 1)

def get_links(url: str):
    """Method doc pending"""
        # Realizamos la petición a la web
    print(f"Empezando: {url}")
    req = requests.get(url)

    # Comprobamos que la petición nos devuelve un Status Code = 200
    status_code = req.status_code
    if status_code == 200:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")

        # Obtenemos todos los divs donde están las entradas
        links = html.find_all('a')
        print(f"Links obtenidos: {len(links)}")
        #print(f"Links: {links}")
        # Recorremos todas las entradas para extraer el título, autor y fecha
        for link in links:
            try:
                href: str = link['href']      # get value of the href attribute
            except TypeError:
                print(f"Main page link sin href: {link}")
                href = ""
            if href:
                # print(f"Link: {href}")
                if href.startswith("http"):
                    print(f"Skipping domain: {href}")
                    links.append(href)
                else:
                    links.append(recursiveUrl(url, link, 1))
        return links


URL = "https://crawler-test.com"
print(get_links(URL))
