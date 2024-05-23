"""Execute the spider and output the result"""
import json
import subprocess

from typing import Final, AnyStr

SCRAPY_SPIDER: Final = "follow_all"
SCRAPY_RESULT_FILE: Final = "follow_all.result.json"


def process_result() -> list[dict]:
    """
    Convert the spider output to a list of dictionaries.
    """
    dictionaries = []
    with open(SCRAPY_RESULT_FILE, "r", encoding="utf8") as f:
        # Slipping the first and last lines (Open and closing brackets)
        lines: list[AnyStr] = f.readlines()[1:-1]
        for line in lines:
            # Strip the last character
            dict_str = line.replace("},", "}")
            # Store the new dict
            dictionaries.append(json.loads(dict_str))
    return dictionaries


def print_header(header: str) -> None:
    """Missing doc"""
    print("-----------------")
    print(f"- {header} -")
    print("-----------------")


def print_links_with_depth(dictionaries: list[dict]) -> None:
    """Print all the links and the depth"""
    print_header("All the links")
    for link in dictionaries:
        print(f"link: {link["link"]} - Depth: {link["depth"]}")
    print("-----------------\n")


def print_error_links(dictionaries: list[dict]) -> None:
    """Print the links with errors"""
    print_header(" Error links ")
    for link in dictionaries:
        if link["error"] != "None":
            print(f"link: {link["link"]}")
    print("-----------------\n")


if __name__ == "__main__":
    process = subprocess.run("scrapy crawl " + SCRAPY_SPIDER + " -o " + SCRAPY_RESULT_FILE)
    if process.returncode == 0:
        dict_result: list[dict] = process_result()
        print_links_with_depth(dict_result)
        print_error_links(dict_result)
    else:
        print(f"Unexpected error: {process.stderr}")
